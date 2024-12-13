"""
Class to hold the state that is waiting to be committed to disk.
"""

from __future__ import annotations

from collections import defaultdict
import contextlib
from dataclasses import dataclass, field, fields
from datetime import datetime

from typing import Any, Dict, List, Optional, Tuple

from hpcflow.sdk.log import TimeIt


class PendingChanges:
    """Class to store pending changes and merge them into a persistent store.

    Parameters
    ----------
    app: App
        The main application context.
    store: PersistentStore
        The persistent store that owns this object
    resource_map: CommitResourceMap
        Map of resources, used when processing commits.
    """

    def __init__(self, app, store, resource_map):
        self.app = app
        self.store = store
        self.resource_map = resource_map

        #: Keys are new task IDs.
        self.add_tasks: Dict[int, AnySTask] = None
        #: Keys are loop IDs, values are loop descriptors.
        self.add_loops: Dict[int, Dict] = None
        #: Keys are submission IDs, values are submission descriptors.
        self.add_submissions: Dict[int, Dict] = None
        #: Keys are element IDs.
        self.add_elements: Dict[int, AnySElement] = None
        #: Keys are element iteration IDs.
        self.add_elem_iters: Dict[int, AnySElementIter] = None
        #: Keys are element action run IDs.
        self.add_EARs: Dict[int, AnySEAR] = None
        #: Keys are parameter indices and values are tuples whose first element is data
        #: to add and whose second element is the source dict for the new data.
        self.add_parameters: Dict[int, AnySParameter] = None
        #: Workflow-related files (inputs, outputs) added to the persistent store.
        self.add_files: List[Dict] = None
        #: Template components to add.
        self.add_template_components: Dict[str, Dict[str, Dict]] = None
        #: Keys are element set IDs, values are descriptors.
        self.add_element_sets: Dict[int, Dict] = None

        #: Keys are task IDs, and values are element IDs to add to that task.
        self.add_elem_IDs: Dict[int, List] = None
        #: Keys are element IDs, and values are iteration IDs to add to that element.
        self.add_elem_iter_IDs: Dict[int, List] = None
        #: Keys are element iteration IDs, then EAR action index, and values are EAR IDs.
        #: This is a list of EAR IDs to add to a given element iteration action.
        self.add_elem_iter_EAR_IDs: Dict[int, Dict[int, List]] = None
        #: Submission parts to add.
        self.add_submission_parts: Dict[int, Dict[str, List[int]]] = None

        #: IDs of EARs to mark as initialised.
        self.set_EARs_initialised: List[int] = None
        #: Submission IDs to attach to EARs.
        self.set_EAR_submission_indices: Dict[int, int] = None
        #: IDs of EARs to mark as skipped.
        self.set_EAR_skips: List[int] = None
        #: Keys are EAR IDs and values are tuples of start time, and start dir snapshot.
        self.set_EAR_starts: Dict[int, Tuple[datetime, Dict], str] = None
        #: Keys are EAR IDs and values are tuples of end time, end dir snapshot, exit
        #: code, and success boolean.
        self.set_EAR_ends: Dict[int, Tuple[datetime, Dict, int, bool]] = None

        #: Keys are IDs of jobscripts.
        self.set_js_metadata: Dict[int, Dict[int, Any]] = None

        #: Keys are IDs of parameters to add or modify.
        self.set_parameters: Dict[int, AnySParameter] = None

        #: Keys are parameter indices and values are dict parameter sources to merge
        #: with existing source of that parameter.
        self.update_param_sources: Dict[int, Dict] = None
        #: Keys are indices of loops, values are descriptions of what to update.
        self.update_loop_indices: Dict[int, Dict[str, int]] = None
        #: Keys are indices of loops, values are number of iterations.
        self.update_loop_num_iters: Dict[int, int] = None
        #: Keys are indices of loops, values are list of parent names.
        self.update_loop_parents: Dict[int, List[str]] = None

        self.reset(is_init=True)  # set up initial data structures

    def __bool__(self):
        """Returns True if there are any outstanding pending items."""
        return (
            bool(self.add_tasks)
            or bool(self.add_loops)
            or bool(self.add_submissions)
            or bool(self.add_elements)
            or bool(self.add_elem_iters)
            or bool(self.add_EARs)
            or bool(self.add_elem_IDs)
            or bool(self.add_elem_iter_IDs)
            or bool(self.add_elem_iter_EAR_IDs)
            or bool(self.add_submission_parts)
            or bool(self.add_parameters)
            or bool(self.add_files)
            or bool(self.add_template_components)
            or bool(self.add_element_sets)
            or bool(self.set_EARs_initialised)
            or bool(self.set_EAR_submission_indices)
            or bool(self.set_EAR_starts)
            or bool(self.set_EAR_ends)
            or bool(self.set_EAR_skips)
            or bool(self.set_js_metadata)
            or bool(self.set_parameters)
            or bool(self.update_param_sources)
            or bool(self.update_loop_indices)
            or bool(self.update_loop_num_iters)
            or bool(self.update_loop_parents)
        )

    def where_pending(self) -> List[str]:
        """
        Get the list of items for which there is some outstanding pending items.
        """
        return [
            k
            for k, v in self.__dict__.items()
            if k not in ("app", "store", "resource_map") and bool(v)
        ]

    @property
    def logger(self):
        """
        The logger.
        """
        return self.app.persistence_logger

    @TimeIt.decorator
    def commit_all(self):
        """Commit all pending changes to disk."""
        self.logger.info(f"committing all pending changes: {self.where_pending()}")

        if not self:
            self.logger.debug("commit: no pending changes to commit.")
            return

        for resources, methods in self.resource_map.groups.items():
            # for each resource, enter `using_resource` context manager in "update" mode:
            with contextlib.ExitStack() as stack:
                for res in resources:
                    # TODO: only enter required resources!
                    stack.enter_context(self.store.using_resource(res, "update"))
                for meth in methods:
                    getattr(self, meth)()

        assert not (self)

    @TimeIt.decorator
    def commit_tasks(self) -> None:
        """Commit pending tasks to disk."""
        if self.add_tasks:
            tasks = self.store.get_tasks_by_IDs(self.add_tasks)
            task_ids = list(self.add_tasks.keys())
            self.logger.debug(f"commit: adding pending tasks with IDs: {task_ids!r}")
            self.store._append_tasks(tasks)
            self.store.num_tasks_cache = None  # invalidate cache
            # pending element IDs that belong to pending tasks are now committed:
            self.add_elem_IDs = {
                k: v for k, v in self.add_elem_IDs.items() if k not in task_ids
            }
        self._clear_add_tasks()

    @TimeIt.decorator
    def commit_loops(self) -> None:
        """Commit pending loops to disk."""
        if self.add_loops:
            # retrieve pending loops, including pending changes to num_added_iterations:
            loops = self.store.get_loops_by_IDs(self.add_loops)
            loop_ids = list(self.add_loops.keys())
            self.logger.debug(f"commit: adding pending loops with indices {loop_ids!r}")
            self.store._append_loops(loops)

            # pending num_added_iters and parents that belong to pending loops are now
            # committed:
            self.update_loop_num_iters = {
                k: v for k, v in self.update_loop_num_iters.items() if k not in loop_ids
            }
            self.update_loop_parents = {
                k: v for k, v in self.update_loop_parents.items() if k not in loop_ids
            }

        self._clear_add_loops()

    @TimeIt.decorator
    def commit_submissions(self) -> None:
        """Commit pending submissions to disk."""
        if self.add_submissions:
            # retrieve pending submissions:
            subs = self.store.get_submissions_by_ID(self.add_submissions)
            sub_ids = list(self.add_submissions.keys())
            self.logger.debug(
                f"commit: adding pending submissions with indices {sub_ids!r}"
            )
            self.store._append_submissions(subs)
        self._clear_add_submissions()

    @TimeIt.decorator
    def commit_submission_parts(self) -> None:
        """
        Commit pending submission parts to disk.
        """
        if self.add_submission_parts:
            self.logger.debug(f"commit: adding pending submission parts")
            self.store._append_submission_parts(self.add_submission_parts)
        self._clear_add_submission_parts()

    @TimeIt.decorator
    def commit_elem_IDs(self) -> None:
        """
        Commit pending element ID updates to disk.
        """
        # TODO: could be batched up?
        for task_ID, elem_IDs in self.add_elem_IDs.items():
            self.logger.debug(
                f"commit: adding pending element IDs to task {task_ID!r}: {elem_IDs!r}."
            )
            self.store._append_task_element_IDs(task_ID, elem_IDs)
            self.store.task_cache.pop(task_ID, None)  # invalidate cache
        self._clear_add_elem_IDs()

    @TimeIt.decorator
    def commit_elements(self) -> None:
        """
        Commit pending elements to disk.
        """
        if self.add_elements:
            elems = self.store.get_elements(self.add_elements)
            elem_ids = list(self.add_elements.keys())
            self.logger.debug(f"commit: adding pending elements with IDs: {elem_ids!r}")
            self.store._append_elements(elems)
            # pending iter IDs that belong to pending elements are now committed:
            self.add_elem_iter_IDs = {
                k: v for k, v in self.add_elem_iter_IDs.items() if k not in elem_ids
            }
        self._clear_add_elements()

    @TimeIt.decorator
    def commit_element_sets(self) -> None:
        """
        Commit pending element sets to disk.
        """
        # TODO: could be batched up?
        for task_id, es_js in self.add_element_sets.items():
            self.logger.debug(f"commit: adding pending element sets.")
            self.store._append_element_sets(task_id, es_js)
        self._clear_add_element_sets()

    @TimeIt.decorator
    def commit_elem_iter_IDs(self) -> None:
        """
        Commit pending element iteration ID updates to disk.
        """
        # TODO: could be batched up?
        for elem_ID, iter_IDs in self.add_elem_iter_IDs.items():
            self.logger.debug(
                f"commit: adding pending element iteration IDs to element {elem_ID!r}: "
                f"{iter_IDs!r}."
            )
            self.store._append_elem_iter_IDs(elem_ID, iter_IDs)
            self.store.element_cache.pop(elem_ID, None)  # invalidate cache
        self._clear_add_elem_iter_IDs()

    @TimeIt.decorator
    def commit_elem_iters(self) -> None:
        """
        Commit pending element iterations to disk.
        """
        if self.add_elem_iters:
            iters = self.store.get_element_iterations(self.add_elem_iters.keys())
            iter_ids = list(self.add_elem_iters.keys())
            self.logger.debug(
                f"commit: adding pending element iterations with IDs: {iter_ids!r}"
            )
            self.store._append_elem_iters(iters)
            # pending EAR IDs that belong to pending iters are now committed:
            self.add_elem_iter_EAR_IDs = {
                k: v for k, v in self.add_elem_iter_EAR_IDs.items() if k not in iter_ids
            }
            # pending EARs_initialised that belong to pending iters are now committed:
            self.set_EARs_initialised = [
                i for i in self.set_EARs_initialised if i not in iter_ids
            ]
        self._clear_add_elem_iters()

    @TimeIt.decorator
    def commit_elem_iter_EAR_IDs(self) -> None:
        """
        Commit pending element action run ID updates to disk.
        """
        # TODO: could be batched up?
        for iter_ID, act_EAR_IDs in self.add_elem_iter_EAR_IDs.items():
            self.logger.debug(
                f"commit: adding pending EAR IDs to element iteration {iter_ID!r}: "
                f"{dict(act_EAR_IDs)!r}."
            )
            for act_idx, EAR_IDs in act_EAR_IDs.items():
                self.store._append_elem_iter_EAR_IDs(iter_ID, act_idx, EAR_IDs)
            self.store.element_iter_cache.pop(iter_ID, None)  # invalidate cache
        self._clear_add_elem_iter_EAR_IDs()

    @TimeIt.decorator
    def commit_EARs(self) -> None:
        """
        Commit pending element action runs to disk.
        """
        if self.add_EARs:
            EARs = self.store.get_EARs(self.add_EARs)
            EAR_ids = list(self.add_EARs.keys())
            self.logger.debug(f"commit: adding pending EARs with IDs: {EAR_ids!r}")
            self.store._append_EARs(EARs)
            self.store.num_EARs_cache = None  # invalidate cache
            # pending start/end times/snapshots, submission indices, and skips that belong
            # to pending EARs are now committed (accounted for in `get_EARs` above):
            self.set_EAR_submission_indices = {
                k: v
                for k, v in self.set_EAR_submission_indices.items()
                if k not in EAR_ids
            }
            self.set_EAR_skips = [i for i in self.set_EAR_skips if i not in EAR_ids]
            self.set_EAR_starts = {
                k: v for k, v in self.set_EAR_starts.items() if k not in EAR_ids
            }
            self.set_EAR_ends = {
                k: v for k, v in self.set_EAR_ends.items() if k not in EAR_ids
            }

        self._clear_add_EARs()

    @TimeIt.decorator
    def commit_EARs_initialised(self) -> None:
        """
        Commit pending element action run init state updates to disk.
        """
        if self.set_EARs_initialised:
            iter_ids = self.set_EARs_initialised
            self.logger.debug(
                f"commit: setting pending `EARs_initialised` for iteration IDs: "
                f"{iter_ids!r}."
            )
            # TODO: could be batched up?
            for i in iter_ids:
                self.store._update_elem_iter_EARs_initialised(i)
                self.store.element_iter_cache.pop(i, None)  # invalidate cache
        self._clear_set_EARs_initialised()

    @TimeIt.decorator
    def commit_EAR_submission_indices(self) -> None:
        """
        Commit pending element action run submission index updates to disk.
        """
        if self.set_EAR_submission_indices:
            self.logger.debug(
                f"commit: updating submission indices: "
                f"{self.set_EAR_submission_indices!r}."
            )
            self.store._update_EAR_submission_indices(self.set_EAR_submission_indices)
            for EAR_ID_i in self.set_EAR_submission_indices.keys():
                self.store.EAR_cache.pop(EAR_ID_i, None)  # invalidate cache
            self._clear_set_EAR_submission_indices()

    @TimeIt.decorator
    def commit_EAR_starts(self) -> None:
        """
        Commit pending element action run start information to disk.
        """
        # TODO: could be batched up?
        for EAR_id, (time, snap, hostname) in self.set_EAR_starts.items():
            self.logger.debug(
                f"commit: adding pending start time ({time!r}), run hostname "
                f"({hostname!r}), and directory snapshot to EAR ID {EAR_id!r}."
            )
            self.store._update_EAR_start(EAR_id, time, snap, hostname)
            self.store.EAR_cache.pop(EAR_id, None)  # invalidate cache
        self._clear_set_EAR_starts()

    @TimeIt.decorator
    def commit_EAR_ends(self) -> None:
        """
        Commit pending element action run finish information to disk.
        """
        # TODO: could be batched up?
        for EAR_id, (time, snap, ext, suc) in self.set_EAR_ends.items():
            self.logger.debug(
                f"commit: adding pending end time ({time!r}), directory snapshot, "
                f"exit code ({ext!r}), and success status {suc!r} to EAR ID {EAR_id!r}."
            )
            self.store._update_EAR_end(EAR_id, time, snap, ext, suc)
            self.store.EAR_cache.pop(EAR_id, None)  # invalidate cache
        self._clear_set_EAR_ends()

    @TimeIt.decorator
    def commit_EAR_skips(self) -> None:
        """
        Commit pending element action skip flags to disk.
        """
        # TODO: could be batched up?
        for EAR_id in self.set_EAR_skips:
            self.logger.debug(f"commit: setting EAR ID {EAR_id!r} as skipped.")
            self.store._update_EAR_skip(EAR_id)
            self.store.EAR_cache.pop(EAR_id, None)  # invalidate cache
        self._clear_set_EAR_skips()

    @TimeIt.decorator
    def commit_js_metadata(self) -> None:
        """
        Commit pending jobscript metadata changes to disk.
        """
        if self.set_js_metadata:
            self.logger.debug(
                f"commit: setting jobscript metadata: {self.set_js_metadata!r}"
            )
            self.store._update_js_metadata(self.set_js_metadata)
        self._clear_set_js_metadata()

    @TimeIt.decorator
    def commit_parameters(self) -> None:
        """Make pending parameters persistent."""
        if self.add_parameters:
            params = self.store.get_parameters(self.add_parameters)
            param_ids = list(self.add_parameters.keys())
            self.logger.debug(f"commit: adding pending parameters IDs: {param_ids!r}")
            self.store._append_parameters(params)
        self._clear_add_parameters()

        if self.set_parameters:
            param_ids = list(self.set_parameters.keys())
            self.logger.debug(f"commit: setting values of parameter IDs {param_ids!r}.")
            self.store._set_parameter_values(self.set_parameters)
            for id_i in param_ids:
                self.store.parameter_cache.pop(id_i, None)

        self._clear_set_parameters()

    @TimeIt.decorator
    def commit_files(self) -> None:
        """Add pending files to the files directory."""
        if self.add_files:
            self.logger.debug(f"commit: adding pending files to the files directory.")
            self.store._append_files(self.add_files)
        self._clear_add_files()

    @TimeIt.decorator
    def commit_template_components(self) -> None:
        """
        Commit pending template components to disk.
        """
        if self.add_template_components:
            self.logger.debug(f"commit: adding template components.")
            self.store._update_template_components(self.store.get_template_components())
        self._clear_add_template_components()

    @TimeIt.decorator
    def commit_param_sources(self) -> None:
        """Make pending changes to parameter sources persistent."""
        if self.update_param_sources:
            param_ids = list(self.update_param_sources.keys())
            self.logger.debug(f"commit: updating sources of parameter IDs {param_ids!r}.")
            self.store._update_parameter_sources(self.update_param_sources)
            for id_i in param_ids:
                self.store.param_sources_cache.pop(id_i, None)  # invalidate cache
            self._clear_update_param_sources()

    @TimeIt.decorator
    def commit_loop_indices(self) -> None:
        """Make pending update to element iteration loop indices persistent."""
        # TODO: batch up
        for iter_ID, loop_idx in self.update_loop_indices.items():
            self.logger.debug(
                f"commit: updating loop indices of iteration ID {iter_ID!r} with "
                f"{loop_idx!r}."
            )
            self.store._update_loop_index(iter_ID, loop_idx)
            self.store.element_iter_cache.pop(iter_ID, None)  # invalidate cache
        self._clear_update_loop_indices()

    @TimeIt.decorator
    def commit_loop_num_iters(self) -> None:
        """Make pending update to the number of loop iterations."""
        for index, num_iters in self.update_loop_num_iters.items():
            self.logger.debug(
                f"commit: updating loop {index!r} number of iterations to {num_iters!r}."
            )
            self.store._update_loop_num_iters(index, num_iters)
        self._clear_update_loop_num_iters()

    @TimeIt.decorator
    def commit_loop_parents(self) -> None:
        """Make pending update to additional loop parents."""
        for index, parents in self.update_loop_parents.items():
            self.logger.debug(f"commit: updating loop {index!r} parents to {parents!r}.")
            self.store._update_loop_parents(index, parents)
        self._clear_update_loop_parents()

    def _clear_add_tasks(self):
        self.add_tasks = {}

    def _clear_add_loops(self):
        self.add_loops = {}

    def _clear_add_submissions(self):
        self.add_submissions = {}

    def _clear_add_submission_parts(self):
        self.add_submission_parts = defaultdict(dict)

    def _clear_add_elements(self):
        self.add_elements = {}

    def _clear_add_element_sets(self):
        self.add_element_sets = defaultdict(list)

    def _clear_add_elem_iters(self):
        self.add_elem_iters = {}

    def _clear_add_EARs(self):
        self.add_EARs = {}

    def _clear_add_elem_IDs(self):
        self.add_elem_IDs = defaultdict(list)

    def _clear_add_elem_iter_IDs(self):
        self.add_elem_iter_IDs = defaultdict(list)

    def _clear_add_elem_iter_EAR_IDs(self):
        self.add_elem_iter_EAR_IDs = defaultdict(lambda: defaultdict(list))

    def _clear_set_EARs_initialised(self):
        self.set_EARs_initialised = []

    def _clear_set_EAR_submission_indices(self):
        self.set_EAR_submission_indices = {}

    def _clear_set_EAR_starts(self):
        self.set_EAR_starts = {}

    def _clear_set_EAR_ends(self):
        self.set_EAR_ends = {}

    def _clear_set_EAR_skips(self):
        self.set_EAR_skips = []

    def _clear_set_js_metadata(self):
        self.set_js_metadata = defaultdict(lambda: defaultdict(dict))

    def _clear_add_parameters(self):
        self.add_parameters = {}

    def _clear_add_files(self):
        self.add_files = []

    def _clear_add_template_components(self):
        self.add_template_components = defaultdict(dict)

    def _clear_set_parameters(self):
        self.set_parameters = {}

    def _clear_update_param_sources(self):
        self.update_param_sources = {}

    def _clear_update_loop_indices(self):
        self.update_loop_indices = defaultdict(dict)

    def _clear_update_loop_num_iters(self):
        self.update_loop_num_iters = {}

    def _clear_update_loop_parents(self):
        self.update_loop_parents = {}

    def reset(self, is_init=False) -> None:
        """Clear all pending data and prepare to accept new pending data."""

        if not is_init and not self:
            # no pending changes
            return

        if not is_init:
            self.logger.info("resetting pending changes.")

        self._clear_add_tasks()
        self._clear_add_loops()
        self._clear_add_submissions()
        self._clear_add_submission_parts()
        self._clear_add_elements()
        self._clear_add_element_sets()
        self._clear_add_elem_iters()
        self._clear_add_EARs()

        self._clear_set_EARs_initialised()
        self._clear_add_elem_IDs()
        self._clear_add_elem_iter_IDs()
        self._clear_add_elem_iter_EAR_IDs()

        self._clear_add_parameters()
        self._clear_add_files()
        self._clear_add_template_components()

        self._clear_set_EAR_submission_indices()
        self._clear_set_EAR_starts()
        self._clear_set_EAR_ends()
        self._clear_set_EAR_skips()

        self._clear_set_js_metadata()
        self._clear_set_parameters()

        self._clear_update_param_sources()
        self._clear_update_loop_indices()
        self._clear_update_loop_num_iters()
        self._clear_update_loop_parents()


@dataclass
class CommitResourceMap:
    """
    Map of :py:class:`PendingChanges` commit method names to store resource labels,
    representing the store resources required by each ``commit_*`` method, for a given
    :py:class:`~.PersistentStore`.

    When :py:meth:`PendingChanges.commit_all` is called, the resources specified will be
    opened in "update" mode, for each ``commit_*`` method.

    Notes
    -----
    Normally only of interest to implementations of persistent stores.
    """

    #: Resources for :py:meth:`~.PendingChanges.commit_tasks`.
    commit_tasks: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_loops`.
    commit_loops: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_submissions`.
    commit_submissions: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_submission_parts`.
    commit_submission_parts: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_elem_IDs`.
    commit_elem_IDs: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_elements`.
    commit_elements: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_element_sets`.
    commit_element_sets: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_elem_iter_IDs`.
    commit_elem_iter_IDs: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_elem_iters`.
    commit_elem_iters: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_elem_iter_EAR_IDs`.
    commit_elem_iter_EAR_IDs: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EARs_initialised`.
    commit_EARs_initialised: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EARs`.
    commit_EARs: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EAR_submission_indices`.
    commit_EAR_submission_indices: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EAR_skips`.
    commit_EAR_skips: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EAR_starts`.
    commit_EAR_starts: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_EAR_ends`.
    commit_EAR_ends: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_js_metadata`.
    commit_js_metadata: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_parameters`.
    commit_parameters: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_files`.
    commit_files: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_template_components`.
    commit_template_components: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_param_sources`.
    commit_param_sources: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_loop_indices`.
    commit_loop_indices: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_loop_num_iters`.
    commit_loop_num_iters: Optional[Tuple[str]] = tuple()
    #: Resources for :py:meth:`~.PendingChanges.commit_loop_parents`.
    commit_loop_parents: Optional[Tuple[str]] = tuple()
    #: A dict whose keys are tuples of resource labels and whose values are lists
    #: of :py:class:`PendingChanges` commit method names that require those resources.
    #:
    #: This grouping allows us to batch up commit methods by resource requirements,
    #: which in turn means we can potentially minimise, e.g., the number of network
    #: requests.
    groups: Dict[Tuple[str], List[str]] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.groups = self._group_by_resource()

    def _group_by_resource(self) -> Dict[Tuple[str], List[str]]:
        """
        Get a dict whose keys are tuples of resource labels and whose values are
        lists of :py:class:`PendingChanges` commit method names that require those
        resource.

        This grouping allows us to batch up commit methods by resource requirements,
        which in turn means we can potentially minimise e.g. the number of network
        requests.
        """
        groups = {}
        cur_res_group = None
        for fld in fields(self):
            if not fld.name.startswith("commit_"):
                continue
            res_labels = getattr(self, fld.name)

            if not cur_res_group:
                # start a new resource group: a mapping between resource labels and the
                # commit methods that require those resources:
                cur_res_group = [list(res_labels), [fld.name]]

            elif not res_labels or set(res_labels).intersection(cur_res_group[0]):
                # there is some overlap between resource labels required in the current
                # group and this commit method, so we merge resource labels and add the
                # new commit method:
                cur_res_group[0] = list(set(cur_res_group[0] + list(res_labels)))
                cur_res_group[1].append(fld.name)

            else:
                # no overlap between resource labels required in the current group and
                # those required by this commit method, so append the current group, and
                # start a new group for this commit method:
                if tuple(cur_res_group[0]) not in groups:
                    groups[tuple(cur_res_group[0])] = []
                groups[tuple(cur_res_group[0])].extend(cur_res_group[1])
                cur_res_group = [list(res_labels), [fld.name]]

        if cur_res_group:
            if tuple(cur_res_group[0]) not in groups:
                groups[tuple(cur_res_group[0])] = []

            groups[tuple(cur_res_group[0])].extend(cur_res_group[1])

        return groups
