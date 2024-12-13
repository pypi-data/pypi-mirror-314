"""
Elements are components of tasks.
"""

from __future__ import annotations
import copy
from dataclasses import dataclass, field
import os
from typing import Any, Dict, List, Optional, Tuple, Union

from valida.conditions import ConditionLike
from valida.rules import Rule

from hpcflow.sdk import app
from hpcflow.sdk.core.errors import UnsupportedOSError, UnsupportedSchedulerError
from hpcflow.sdk.core.json_like import ChildObjectSpec, JSONLike
from hpcflow.sdk.core.parallel import ParallelMode
from hpcflow.sdk.core.utils import (
    check_valid_py_identifier,
    dict_values_process_flat,
    get_enum_by_name_or_val,
    split_param_label,
)
from hpcflow.sdk.log import TimeIt
from hpcflow.sdk.submission.shells import get_shell


class _ElementPrefixedParameter:
    _app_attr = "_app"

    def __init__(
        self,
        prefix: str,
        element_iteration: Optional[app.Element] = None,
        element_action: Optional[app.ElementAction] = None,
        element_action_run: Optional[app.ElementActionRun] = None,
    ) -> None:
        self._prefix = prefix
        self._element_iteration = element_iteration
        self._element_action = element_action
        self._element_action_run = element_action_run

        self._prefixed_names_unlabelled = None  # assigned on first access

    def __getattr__(self, name):
        if name not in self.prefixed_names_unlabelled:
            raise ValueError(
                f"No {self._prefix} named {name!r}. Available {self._prefix} are: "
                f"{self.prefixed_names_unlabelled_str}."
            )

        labels = self.prefixed_names_unlabelled.get(name)
        if labels:
            # is multiple; return a dict of `ElementParameter`s
            out = {}
            for label_i in labels:
                path_i = f"{self._prefix}.{name}[{label_i}]"
                out[label_i] = self._app.ElementParameter(
                    path=path_i,
                    task=self._task,
                    parent=self._parent,
                    element=self._element_iteration_obj,
                )

        else:
            # could be labelled still, but with `multiple=False`
            path_i = f"{self._prefix}.{name}"
            out = self._app.ElementParameter(
                path=path_i,
                task=self._task,
                parent=self._parent,
                element=self._element_iteration_obj,
            )
        return out

    def __dir__(self):
        return super().__dir__() + self.prefixed_names_unlabelled

    @property
    def _parent(self):
        return self._element_iteration or self._element_action or self._element_action_run

    @property
    def _element_iteration_obj(self):
        if self._element_iteration:
            return self._element_iteration
        else:
            return self._parent.element_iteration

    @property
    def _task(self):
        return self._parent.task

    @property
    def prefixed_names_unlabelled(self) -> Dict[str, List[str]]:
        """
        A mapping between input types and associated labels.

        If the schema input for a given input type has `multiple=False` (even if a label
        is defined), the values for that input type will be an empty list.

        """
        if self._prefixed_names_unlabelled is None:
            self._prefixed_names_unlabelled = self._get_prefixed_names_unlabelled()
        return self._prefixed_names_unlabelled

    @property
    def prefixed_names_unlabelled_str(self):
        """
        A description of the prefixed names.
        """
        return ", ".join(i for i in self.prefixed_names_unlabelled)

    def __repr__(self):
        # If there are one or more labels present, then replace with a single name
        # indicating there could be multiple (using a `*` prefix):
        names = []
        for unlabelled, labels in self.prefixed_names_unlabelled.items():
            name_i = unlabelled
            if labels:
                name_i = "*" + name_i
            names.append(name_i)
        names_str = ", ".join(i for i in names)
        return f"{self.__class__.__name__}({names_str})"

    def _get_prefixed_names(self):
        return sorted(self._parent.get_parameter_names(self._prefix))

    def _get_prefixed_names_unlabelled(self) -> Dict[str, List[str]]:
        names = self._get_prefixed_names()
        all_names = {}
        for i in list(names):
            if "[" in i:
                unlab_i, label_i = split_param_label(i)
                if unlab_i not in all_names:
                    all_names[unlab_i] = []
                all_names[unlab_i].append(label_i)
            else:
                all_names[i] = []
        return all_names

    def __iter__(self):
        for name in self.prefixed_names_unlabelled:
            yield getattr(self, name)


class ElementInputs(_ElementPrefixedParameter):
    """
    The inputs to an element.

    Parameters
    ----------
    element_iteration: ElementIteration
        Which iteration does this refer to?
    element_action: ~hpcflow.app.ElementAction
        Which action does this refer to?
    element_action_run: ~hpcflow.app.ElementActionRun
        Which EAR does this refer to?
    """

    def __init__(
        self,
        element_iteration: Optional[app.ElementIteration] = None,
        element_action: Optional[app.ElementAction] = None,
        element_action_run: Optional[app.ElementActionRun] = None,
    ) -> None:
        super().__init__("inputs", element_iteration, element_action, element_action_run)


class ElementOutputs(_ElementPrefixedParameter):
    """
    The outputs from an element.

    Parameters
    ----------
    element_iteration: ElementIteration
        Which iteration does this refer to?
    element_action: ~hpcflow.app.ElementAction
        Which action does this refer to?
    element_action_run: ~hpcflow.app.ElementActionRun
        Which EAR does this refer to?
    """

    def __init__(
        self,
        element_iteration: Optional[app.ElementIteration] = None,
        element_action: Optional[app.ElementAction] = None,
        element_action_run: Optional[app.ElementActionRun] = None,
    ) -> None:
        super().__init__("outputs", element_iteration, element_action, element_action_run)


class ElementInputFiles(_ElementPrefixedParameter):
    """
    The input files to an element.

    Parameters
    ----------
    element_iteration: ElementIteration
        Which iteration does this refer to?
    element_action: ~hpcflow.app.ElementAction
        Which action does this refer to?
    element_action_run: ~hpcflow.app.ElementActionRun
        Which EAR does this refer to?
    """

    def __init__(
        self,
        element_iteration: Optional[app.ElementIteration] = None,
        element_action: Optional[app.ElementAction] = None,
        element_action_run: Optional[app.ElementActionRun] = None,
    ) -> None:
        super().__init__(
            "input_files", element_iteration, element_action, element_action_run
        )


class ElementOutputFiles(_ElementPrefixedParameter):
    """
    The output files from an element.

    Parameters
    ----------
    element_iteration: ElementIteration
        Which iteration does this refer to?
    element_action: ~hpcflow.app.ElementAction
        Which action does this refer to?
    element_action_run: ~hpcflow.app.ElementActionRun
        Which EAR does this refer to?
    """

    def __init__(
        self,
        element_iteration: Optional[app.ElementIteration] = None,
        element_action: Optional[app.ElementAction] = None,
        element_action_run: Optional[app.ElementActionRun] = None,
    ) -> None:
        super().__init__(
            "output_files", element_iteration, element_action, element_action_run
        )


@dataclass
class ElementResources(JSONLike):
    """
    The resources an element requires.

    Note
    ----
    It is common to leave most of these unspecified.
    Many of them have complex interactions with each other.

    Parameters
    ----------
    scratch: str
        Which scratch space to use.
    parallel_mode: ParallelMode
        Which parallel mode to use.
    num_cores: int
        How many cores to request.
    num_cores_per_node: int
        How many cores per compute node to request.
    num_threads: int
        How many threads to request.
    num_nodes: int
        How many compute nodes to request.
    scheduler: str
        Which scheduler to use.
    shell: str
        Which system shell to use.
    use_job_array: bool
        Whether to use array jobs.
    max_array_items: int
        If using array jobs, up to how many items should be in the job array.
    time_limit: str
        How long to run for.
    scheduler_args: dict[str, Any]
        Additional arguments to pass to the scheduler.
    shell_args: dict[str, Any]
        Additional arguments to pass to the shell.
    os_name: str
        Which OS to use.
    environments: dict
        Which execution environments to use.
    SGE_parallel_env: str
        Which SGE parallel environment to request.
    SLURM_partition: str
        Which SLURM partition to request.
    SLURM_num_tasks: str
        How many SLURM tasks to request.
    SLURM_num_tasks_per_node: str
        How many SLURM tasks per compute node to request.
    SLURM_num_nodes: str
        How many compute nodes to request.
    SLURM_num_cpus_per_task: str
        How many CPU cores to ask for per SLURM task.
    """

    # TODO: how to specify e.g. high-memory requirement?

    #: Which scratch space to use.
    scratch: Optional[str] = None
    #: Which parallel mode to use.
    parallel_mode: Optional[ParallelMode] = None
    #: How many cores to request.
    num_cores: Optional[int] = None
    #: How many cores per compute node to request.
    num_cores_per_node: Optional[int] = None
    #: How many threads to request.
    num_threads: Optional[int] = None
    #: How many compute nodes to request.
    num_nodes: Optional[int] = None

    #: Which scheduler to use.
    scheduler: Optional[str] = None
    #: Which system shell to use.
    shell: Optional[str] = None
    #: Whether to use array jobs.
    use_job_array: Optional[bool] = None
    #: If using array jobs, up to how many items should be in the job array.
    max_array_items: Optional[int] = None
    #: How long to run for.
    time_limit: Optional[str] = None
    #: Additional arguments to pass to the scheduler.
    scheduler_args: Optional[Dict] = None
    #: Additional arguments to pass to the shell.
    shell_args: Optional[Dict] = None
    #: Which OS to use.
    os_name: Optional[str] = None
    #: Which execution environments to use.
    environments: Optional[Dict] = None

    # SGE scheduler specific:
    #: Which SGE parallel environment to request.
    SGE_parallel_env: str = None

    # SLURM scheduler specific:
    #: Which SLURM partition to request.
    SLURM_partition: str = None
    #: How many SLURM tasks to request.
    SLURM_num_tasks: str = None
    #: How many SLURM tasks per compute node to request.
    SLURM_num_tasks_per_node: str = None
    #: How many compute nodes to request.
    SLURM_num_nodes: str = None
    #: How many CPU cores to ask for per SLURM task.
    SLURM_num_cpus_per_task: str = None

    def __post_init__(self):
        if (
            self.num_cores is None
            and self.num_cores_per_node is None
            and self.num_threads is None
            and self.num_nodes is None
        ):
            self.num_cores = 1

        if self.parallel_mode:
            self.parallel_mode = get_enum_by_name_or_val(ParallelMode, self.parallel_mode)

        self.scheduler_args = self.scheduler_args or {}
        self.shell_args = self.shell_args or {}

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        else:
            return self.__dict__ == other.__dict__

    def get_jobscript_hash(self):
        """Get hash from all arguments that distinguish jobscripts."""

        def _hash_dict(d):
            if not d:
                return -1
            keys, vals = zip(*d.items())
            return hash(tuple((keys, vals)))

        exclude = ("time_limit",)
        dct = {k: copy.deepcopy(v) for k, v in self.__dict__.items() if k not in exclude}

        scheduler_args = dct["scheduler_args"]
        shell_args = dct["shell_args"]
        envs = dct["environments"]

        if isinstance(scheduler_args, dict):
            if "options" in scheduler_args:
                dct["scheduler_args"]["options"] = _hash_dict(scheduler_args["options"])
            dct["scheduler_args"] = _hash_dict(dct["scheduler_args"])

        if isinstance(shell_args, dict):
            dct["shell_args"] = _hash_dict(shell_args)

        if isinstance(envs, dict):
            for k, v in envs.items():
                dct["environments"][k] = _hash_dict(v)
            dct["environments"] = _hash_dict(dct["environments"])

        return _hash_dict(dct)

    @property
    def is_parallel(self) -> bool:
        """Returns True if any scheduler-agnostic arguments indicate a parallel job."""
        return (
            (self.num_cores and self.num_cores != 1)
            or (self.num_cores_per_node and self.num_cores_per_node != 1)
            or (self.num_nodes and self.num_nodes != 1)
            or (self.num_threads and self.num_threads != 1)
        )

    @property
    def SLURM_is_parallel(self) -> bool:
        """Returns True if any SLURM-specific arguments indicate a parallel job."""
        return (
            (self.SLURM_num_tasks and self.SLURM_num_tasks != 1)
            or (self.SLURM_num_tasks_per_node and self.SLURM_num_tasks_per_node != 1)
            or (self.SLURM_num_nodes and self.SLURM_num_nodes != 1)
            or (self.SLURM_num_cpus_per_task and self.SLURM_num_cpus_per_task != 1)
        )

    @staticmethod
    def get_env_instance_filterable_attributes() -> Tuple[str]:
        """Get a tuple of resource attributes that are used to filter environment
        executable instances at submit- and run-time."""
        return ("num_cores",)  # TODO: filter on `parallel_mode` later

    @staticmethod
    def get_default_os_name():
        """
        Get the default value for OS name.
        """
        return os.name

    @classmethod
    def get_default_shell(cls):
        """
        Get the default value for name.
        """
        return cls.app.config.default_shell

    @classmethod
    def get_default_scheduler(cls, os_name, shell_name):
        """
        Get the default value for scheduler.
        """
        if os_name == "nt" and "wsl" in shell_name:
            # provide a "*_posix" default scheduler on windows if shell is WSL:
            return "direct_posix"
        return cls.app.config.default_scheduler

    def set_defaults(self):
        """
        Set defaults for unspecified values that need defaults.
        """
        if self.os_name is None:
            self.os_name = self.get_default_os_name()
        if self.shell is None:
            self.shell = self.get_default_shell()
        if self.scheduler is None:
            self.scheduler = self.get_default_scheduler(self.os_name, self.shell)

        # merge defaults shell args from config:
        self.shell_args = {
            **self.app.config.shells.get(self.shell, {}).get("defaults", {}),
            **self.shell_args,
        }

        # "direct_posix" scheduler is valid on Windows if using WSL:
        cfg_lookup = f"{self.scheduler}_posix" if "wsl" in self.shell else self.scheduler
        cfg_sched = copy.deepcopy(self.app.config.schedulers.get(cfg_lookup, {}))

        # merge defaults scheduler args from config:
        cfg_defs = cfg_sched.get("defaults", {})
        cfg_opts = cfg_defs.pop("options", {})
        opts = {**cfg_opts, **self.scheduler_args.get("options", {})}
        self.scheduler_args["options"] = opts
        self.scheduler_args = {**cfg_defs, **self.scheduler_args}

    def validate_against_machine(self):
        """Validate the values for `os_name`, `shell` and `scheduler` against those
        supported on this machine (as specified by the app configuration)."""
        if self.os_name != os.name:
            raise UnsupportedOSError(os_name=self.os_name)
        if self.scheduler not in self.app.config.schedulers:
            raise UnsupportedSchedulerError(
                scheduler=self.scheduler,
                supported=self.app.config.schedulers,
            )
        # might raise `UnsupportedShellError`:
        get_shell(shell_name=self.shell, os_name=self.os_name)

        # Validate num_cores/num_nodes against options in config and set scheduler-
        # specific resources (e.g. SGE parallel environmentPE, and SLURM partition)
        if "_" in self.scheduler:  # e.g. WSL on windows uses *_posix
            key = tuple(self.scheduler.split("_"))
        else:
            key = (self.scheduler.lower(), self.os_name.lower())
        scheduler_cls = self.app.scheduler_lookup[key]
        scheduler_cls.process_resources(self, self.app.config.schedulers[self.scheduler])


class ElementIteration:
    """
    A particular iteration of an element.

    Parameters
    ----------
    id_ : int
        The ID of this iteration.
    is_pending: bool
        Whether this iteration is pending execution.
    index: int
        The index of this iteration in its parent element.
    element: Element
        The element this is an iteration of.
    data_idx: dict
        The overall element iteration data index, before resolution of EARs.
    EARs_initialised: bool
        Whether EARs have been set up for the iteration.
    EAR_IDs: dict[int, int]
        Mapping from iteration number to EAR ID, where known.
    EARs: list[dict]
        Data about EARs.
    schema_parameters: list[str]
        Parameters from the schema.
    loop_idx: dict[str, int]
        Indexing information from the loop.
    """

    _app_attr = "app"

    def __init__(
        self,
        id_: int,
        is_pending: bool,
        index: int,
        element: app.Element,
        data_idx: Dict,
        EARs_initialised: bool,
        EAR_IDs: Dict[int, int],
        EARs: Union[List[Dict], None],
        schema_parameters: List[str],
        loop_idx: Dict,
    ):
        self._id = id_
        self._is_pending = is_pending
        self._index = index
        self._element = element
        self._data_idx = data_idx
        self._loop_idx = loop_idx
        self._schema_parameters = schema_parameters
        self._EARs_initialised = EARs_initialised
        self._EARs = EARs
        self._EAR_IDs = EAR_IDs

        # assigned on first access of corresponding properties:
        self._inputs = None
        self._outputs = None
        self._input_files = None
        self._output_files = None
        self._action_objs = None

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id_!r}, "
            f"index={self.index!r}, element={self.element!r}, "
            f"EARs_initialised={self.EARs_initialised!r}"
            f")"
        )

    @property
    def data_idx(self):
        """The overall element iteration data index, before resolution of EARs."""
        return self._data_idx

    @property
    def EARs_initialised(self):
        """Whether or not the EARs have been initialised."""
        return self._EARs_initialised

    @property
    def element(self):
        """
        The element this is an iteration of.
        """
        return self._element

    @property
    def index(self):
        """
        The index of this iteration in its parent element.
        """
        return self._index

    @property
    def id_(self) -> int:
        """
        The ID of this iteration.
        """
        return self._id

    @property
    def is_pending(self) -> bool:
        """
        Whether this iteration is pending execution.
        """
        return self._is_pending

    @property
    def task(self):
        """
        The task this is an iteration of an element for.
        """
        return self.element.task

    @property
    def workflow(self):
        """
        The workflow this is a part of.
        """
        return self.element.workflow

    @property
    def loop_idx(self) -> Dict[str, int]:
        """
        Indexing information from the loop.
        """
        return self._loop_idx

    @property
    def schema_parameters(self) -> List[str]:
        """
        Parameters from the schema.
        """
        return self._schema_parameters

    @property
    def EAR_IDs(self) -> Dict[int, int]:
        """
        Mapping from iteration number to EAR ID, where known.
        """
        return self._EAR_IDs

    @property
    def EAR_IDs_flat(self):
        """
        The EAR IDs.
        """
        return [j for i in self.EAR_IDs.values() for j in i]

    @property
    def actions(self) -> Dict[app.ElementAction]:
        """
        The actions of this iteration.
        """
        if self._action_objs is None:
            self._action_objs = {
                act_idx: self.app.ElementAction(
                    element_iteration=self,
                    action_idx=act_idx,
                    runs=runs,
                )
                for act_idx, runs in (self._EARs or {}).items()
            }
        return self._action_objs

    @property
    def action_runs(self) -> List[app.ElementActionRun]:
        """
        A list of element action runs, where only the final run is taken for each
        element action.
        """
        return [i.runs[-1] for i in self.actions.values()]

    @property
    def inputs(self) -> app.ElementInputs:
        """
        The inputs to this element.
        """
        if not self._inputs:
            self._inputs = self.app.ElementInputs(element_iteration=self)
        return self._inputs

    @property
    def outputs(self) -> app.ElementOutputs:
        """
        The outputs from this element.
        """
        if not self._outputs:
            self._outputs = self.app.ElementOutputs(element_iteration=self)
        return self._outputs

    @property
    def input_files(self) -> app.ElementInputFiles:
        """
        The input files to this element.
        """
        if not self._input_files:
            self._input_files = self.app.ElementInputFiles(element_iteration=self)
        return self._input_files

    @property
    def output_files(self) -> app.ElementOutputFiles:
        """
        The output files from this element.
        """
        if not self._output_files:
            self._output_files = self.app.ElementOutputFiles(element_iteration=self)
        return self._output_files

    def get_parameter_names(self, prefix: str) -> List[str]:
        """Get parameter types associated with a given prefix.

        For example, with the prefix "inputs", this would return `['p1', 'p2']` for a task
        schema that has input types `p1` and `p2`. For inputs, labels are ignored. For
        example, for a task schema that accepts two inputs of the same type `p1`, with
        labels `one` and `two`, this method would return (for the "inputs" prefix):
        `['p1[one]', 'p1[two]']`.

        This method is distinct from `Action.get_parameter_names` in that it returns
        schema-level inputs/outputs, whereas `Action.get_parameter_names` returns
        action-level input/output/file types/labels.

        Parameters
        ----------
        prefix
            One of "inputs", "outputs".

        """
        single_label_lookup = self.task.template._get_single_label_lookup("inputs")
        return list(
            ".".join(single_label_lookup.get(i, i).split(".")[1:])
            for i in self.schema_parameters
            if i.startswith(prefix)
        )

    @TimeIt.decorator
    def get_data_idx(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
    ) -> Dict[str, int]:
        """
        Get the data index.

        Parameters
        ----------
        path:
            If specified, filters the data indices to the ones relevant to this path.
        action_idx:
            The index of the action within the schema.
        run_idx:
            The index of the run within the action.
        """

        if not self.actions:
            data_idx = self.data_idx

        elif action_idx is None:
            # inputs should be from first action where that input is defined, and outputs
            # should include modifications from all actions; we can't just take
            # `self.data_idx`, because 1) this is used for initial runs, and subsequent
            # runs might have different parametrisations, and 2) we want to include
            # intermediate input/output_files:
            data_idx = {}
            for action in self.actions.values():
                for k, v in action.runs[run_idx].data_idx.items():
                    is_input = k.startswith("inputs")
                    if (is_input and k not in data_idx) or not is_input:
                        data_idx[k] = v

        else:
            elem_act = self.actions[action_idx]
            data_idx = elem_act.runs[run_idx].data_idx

        if path:
            data_idx = {k: v for k, v in data_idx.items() if k.startswith(path)}

        return copy.deepcopy(data_idx)

    @TimeIt.decorator
    def get_parameter_sources(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
        typ: str = None,
        as_strings: bool = False,
        use_task_index: bool = False,
    ) -> Dict[str, Union[str, Dict[str, Any]]]:
        """
        Get the origin of parameters.

        Parameters
        ----------
        use_task_index
            If True, use the task index within the workflow, rather than the task insert
            ID.
        """
        data_idx = self.get_data_idx(path, action_idx, run_idx)

        # the value associated with `repeats.*` is the repeats index, not a parameter ID:
        for k in list(data_idx.keys()):
            if k.startswith("repeats."):
                data_idx.pop(k)

        out = dict_values_process_flat(
            data_idx,
            callable=self.workflow.get_parameter_sources,
        )
        task_key = "task_insert_ID"

        if use_task_index:
            task_key = "task_idx"
            out_task_idx = {}
            for k, v in out.items():
                insert_ID = v.pop("task_insert_ID", None)
                if insert_ID is not None:
                    v[task_key] = self.workflow.tasks.get(insert_ID=insert_ID).index
                out_task_idx[k] = v
            out = out_task_idx

        if typ:
            out_ = {}
            for k, v in out.items():
                is_multi = False
                if isinstance(v, list):
                    is_multi = True
                else:
                    v = [v]

                sources_k = []
                for src_i in v:
                    if src_i["type"] == typ:
                        if not is_multi:
                            sources_k = src_i
                            break
                        else:
                            sources_k.append(src_i)

                if sources_k:
                    out_[k] = sources_k

            out = out_

        if as_strings:
            # format as a dict with compact string values
            self_task_val = (
                self.task.index if task_key == "task_idx" else self.task.insert_ID
            )
            out_strs = {}
            for k, v in out.items():
                if v["type"] == "local_input":
                    if v[task_key] == self_task_val:
                        out_strs[k] = "local"
                    else:
                        out_strs[k] = f"task.{v[task_key]}.input"
                elif v["type"] == "default_input":
                    out_strs == "default"
                else:
                    out_strs[k] = (
                        f"task.{v[task_key]}.element.{v['element_idx']}."
                        f"action.{v['action_idx']}.run.{v['run_idx']}"
                    )
            out = out_strs

        return out

    @TimeIt.decorator
    def get(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
        default: Any = None,
        raise_on_missing: bool = False,
        raise_on_unset: bool = False,
    ) -> Any:
        """Get element data from the persistent store."""
        # TODO include a "stats" parameter which when set we know the run has been
        # executed (or if start time is set but not end time, we know it's running or
        # failed.)

        data_idx = self.get_data_idx(action_idx=action_idx, run_idx=run_idx)
        single_label_lookup = self.task.template._get_single_label_lookup(prefix="inputs")

        if single_label_lookup:
            # For any non-multiple `SchemaParameter`s of this task with non-empty labels,
            # remove the trivial label:
            for key in list(data_idx.keys()):
                if (path or "").startswith(key):
                    # `path` uses labelled type, so no need to convert to non-labelled
                    continue
                lookup_val = single_label_lookup.get(key)
                if lookup_val:
                    data_idx[lookup_val] = data_idx.pop(key)

        return self.task._get_merged_parameter_data(
            data_index=data_idx,
            path=path,
            raise_on_missing=raise_on_missing,
            raise_on_unset=raise_on_unset,
            default=default,
        )

    @TimeIt.decorator
    def get_EAR_dependencies(
        self,
        as_objects: Optional[bool] = False,
    ) -> List[Union[int, app.ElementActionRun]]:
        """Get EARs that this element iteration depends on (excluding EARs of this element
        iteration)."""
        # TODO: test this includes EARs of upstream iterations of this iteration's element
        if self.action_runs:
            out = sorted(
                set(
                    EAR_ID
                    for i in self.action_runs
                    for EAR_ID in i.get_EAR_dependencies(as_objects=False)
                    if not EAR_ID in self.EAR_IDs_flat
                )
            )
        else:
            # if an "input-only" task schema, then there will be no action runs, but the
            # ElementIteration can still depend on other EARs if inputs are sourced from
            # upstream tasks:
            out = []
            for src in self.get_parameter_sources(typ="EAR_output").values():
                if not isinstance(src, list):
                    src = [src]
                for src_i in src:
                    EAR_ID_i = src_i["EAR_ID"]
                    out.append(EAR_ID_i)
            out = sorted(set(out))

        if as_objects:
            out = self.workflow.get_EARs_from_IDs(out)
        return out

    @TimeIt.decorator
    def get_element_iteration_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementIteration]]:
        """Get element iterations that this element iteration depends on."""
        # TODO: test this includes previous iterations of this iteration's element
        EAR_IDs = self.get_EAR_dependencies(as_objects=False)
        out = sorted(set(self.workflow.get_element_iteration_IDs_from_EAR_IDs(EAR_IDs)))
        if as_objects:
            out = self.workflow.get_element_iterations_from_IDs(out)
        return out

    @TimeIt.decorator
    def get_element_dependencies(
        self,
        as_objects: Optional[bool] = False,
    ) -> List[Union[int, app.Element]]:
        """Get elements that this element iteration depends on."""
        # TODO: this will be used in viz.
        EAR_IDs = self.get_EAR_dependencies(as_objects=False)
        out = sorted(set(self.workflow.get_element_IDs_from_EAR_IDs(EAR_IDs)))
        if as_objects:
            out = self.workflow.get_elements_from_IDs(out)
        return out

    def get_input_dependencies(self) -> Dict[str, Dict]:
        """Get locally defined inputs/sequences/defaults from other tasks that this
        element iteration depends on."""
        out = {}
        for k, v in self.get_parameter_sources().items():
            if not isinstance(v, list):
                v = [v]
            for v_i in v:
                if (
                    v_i["type"] in ["local_input", "default_input"]
                    and v_i["task_insert_ID"] != self.task.insert_ID
                ):
                    out[k] = v_i

        return out

    def get_task_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.WorkflowTask]]:
        """Get tasks (insert ID or WorkflowTask objects) that this element iteration
        depends on.

        Dependencies may come from either elements from upstream tasks, or from locally
        defined inputs/sequences/defaults from upstream tasks."""

        out = self.workflow.get_task_IDs_from_element_IDs(
            self.get_element_dependencies(as_objects=False)
        )
        for i in self.get_input_dependencies().values():
            out.append(i["task_insert_ID"])

        out = sorted(set(out))

        if as_objects:
            out = [self.workflow.tasks.get(insert_ID=i) for i in out]

        return out

    @TimeIt.decorator
    def get_dependent_EARs(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementActionRun]]:
        """Get EARs of downstream iterations and tasks that depend on this element
        iteration."""
        # TODO: test this includes EARs of downstream iterations of this iteration's element
        deps = []
        for task in self.workflow.tasks[self.task.index :]:
            for elem in task.elements[:]:
                for iter_ in elem.iterations:
                    if iter_.id_ == self.id_:
                        # don't include EARs of this iteration
                        continue
                    for run in iter_.action_runs:
                        for dep_EAR_i in run.get_EAR_dependencies(as_objects=True):
                            # does dep_EAR_i belong to self?
                            if dep_EAR_i.id_ in self.EAR_IDs_flat and run.id_ not in deps:
                                deps.append(run.id_)
        deps = sorted(deps)
        if as_objects:
            deps = self.workflow.get_EARs_from_IDs(deps)

        return deps

    @TimeIt.decorator
    def get_dependent_element_iterations(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementIteration]]:
        """Get elements iterations of downstream iterations and tasks that depend on this
        element iteration."""
        # TODO: test this includes downstream iterations of this iteration's element?
        deps = []
        for task in self.workflow.tasks[self.task.index :]:
            for elem in task.elements[:]:
                for iter_i in elem.iterations:
                    if iter_i.id_ == self.id_:
                        continue
                    for dep_iter_i in iter_i.get_element_iteration_dependencies(
                        as_objects=True
                    ):
                        if dep_iter_i.id_ == self.id_ and iter_i.id_ not in deps:
                            deps.append(iter_i.id_)
        deps = sorted(deps)
        if as_objects:
            deps = self.workflow.get_element_iterations_from_IDs(deps)

        return deps

    @TimeIt.decorator
    def get_dependent_elements(
        self,
        as_objects: bool = False,
    ) -> List[Union[int, app.Element]]:
        """Get elements of downstream tasks that depend on this element iteration."""
        deps = []
        for task in self.task.downstream_tasks:
            for element in task.elements[:]:
                for iter_i in element.iterations:
                    for dep_iter_i in iter_i.get_element_iteration_dependencies(
                        as_objects=True
                    ):
                        if dep_iter_i.id_ == self.id_ and element.id_ not in deps:
                            deps.append(element.id_)

        deps = sorted(deps)
        if as_objects:
            deps = self.workflow.get_elements_from_IDs(deps)

        return deps

    def get_dependent_tasks(
        self,
        as_objects: bool = False,
    ) -> List[Union[int, app.WorkflowTask]]:
        """Get downstream tasks that depend on this element iteration."""
        deps = []
        for task in self.task.downstream_tasks:
            for element in task.elements[:]:
                for iter_i in element.iterations:
                    for dep_iter_i in iter_i.get_element_iteration_dependencies(
                        as_objects=True
                    ):
                        if dep_iter_i.id_ == self.id_ and task.insert_ID not in deps:
                            deps.append(task.insert_ID)
        deps = sorted(deps)
        if as_objects:
            deps = [self.workflow.tasks.get(insert_ID=i) for i in deps]

        return deps

    def get_template_resources(self) -> Dict:
        """Get template-level resources."""
        out = {}
        for res_i in self.workflow.template.resources:
            out[res_i.scope.to_string()] = res_i._get_value()
        return out

    @TimeIt.decorator
    def get_resources(self, action: app.Action, set_defaults: bool = False) -> Dict:
        """Resolve specific resources for the specified action of this iteration,
        considering all applicable scopes.

        Parameters
        ----------
        set_defaults
            If `True`, include machine-defaults for `os_name`, `shell` and `scheduler`.

        """

        # This method is currently accurate for both `ElementIteration` and `EAR` objects
        # because when generating the EAR data index we copy (from the schema data index)
        # anything that starts with "resources". BUT: when we support adding a run, the
        # user should be able to modify the resources! Which would invalidate this
        # assumption!!!!!

        # --- so need to rethink...
        # question is perhaps "what would the resources be if this action were to become
        # an EAR?" which would then allow us to test a resources-based action rule.

        resource_specs = copy.deepcopy(self.get("resources"))

        env_spec = action.get_environment_spec()
        env_name = env_spec["name"]

        # set default env specifiers, if none set:
        if "any" not in resource_specs:
            resource_specs["any"] = {}
        if "environments" not in resource_specs["any"]:
            resource_specs["any"]["environments"] = {env_name: copy.deepcopy(env_spec)}

        for scope, dat in resource_specs.items():
            if "environments" in dat:
                # keep only relevant user-provided environment specifiers:
                resource_specs[scope]["environments"] = {
                    k: v for k, v in dat["environments"].items() if k == env_name
                }
                # merge user-provided specifiers into action specifiers:
                resource_specs[scope]["environments"][env_name] = {
                    **resource_specs[scope]["environments"].get(env_name, {}),
                    **copy.deepcopy(env_spec),
                }

        resources = {}
        for scope in action.get_possible_scopes()[::-1]:
            # loop in reverse so higher-specificity scopes take precedence:
            scope_s = scope.to_string()
            scope_res = resource_specs.get(scope_s, {})
            resources.update({k: v for k, v in scope_res.items() if v is not None})

        if set_defaults:
            # used in e.g. `Rule.test` if testing resource rules on element iterations:
            if "os_name" not in resources:
                resources["os_name"] = self.app.ElementResources.get_default_os_name()
            if "shell" not in resources:
                resources["shell"] = self.app.ElementResources.get_default_shell()
            if "scheduler" not in resources:
                resources["scheduler"] = self.app.ElementResources.get_default_scheduler(
                    resources["os_name"], resources["shell"]
                )

        return resources

    def get_resources_obj(
        self, action: app.Action, set_defaults: bool = False
    ) -> app.ElementResources:
        """
        Get the resources for an action (see :py:meth:`get_resources`)
        as a searchable model.
        """
        return self.app.ElementResources(**self.get_resources(action, set_defaults))


class Element:
    """
    A basic component of a workflow. Elements are enactments of tasks.

    Parameters
    ----------
    id_ : int
        The ID of this element.
    is_pending: bool
        Whether this element is pending execution.
    task: ~hpcflow.app.WorkflowTask
        The task this is part of the enactment of.
    index: int
        The index of this element.
    es_idx: int
        The index within the task of the element set containing this element.
    seq_idx: dict[str, int]
        The sequence index IDs.
    src_idx: dict[str, int]
        The input source indices.
    iteration_IDs: list[int]
        The known IDs of iterations,
    iterations: list[dict]
        Data for creating iteration objects.
    """

    _app_attr = "app"

    # TODO: use slots
    # TODO:
    #   - add `iterations` property which returns `ElementIteration`
    #   - also map iteration properties of the most recent iteration to this object

    def __init__(
        self,
        id_: int,
        is_pending: bool,
        task: app.WorkflowTask,
        index: int,
        es_idx: int,
        seq_idx: Dict[str, int],
        src_idx: Dict[str, int],
        iteration_IDs: List[int],
        iterations: List[Dict],
    ) -> None:
        self._id = id_
        self._is_pending = is_pending
        self._task = task
        self._index = index
        self._es_idx = es_idx
        self._seq_idx = seq_idx
        self._src_idx = src_idx

        self._iteration_IDs = iteration_IDs
        self._iterations = iterations

        # assigned on first access:
        self._iteration_objs = None

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id_!r}, "
            f"index={self.index!r}, task={self.task.unique_name!r}"
            f")"
        )

    @property
    def id_(self) -> int:
        """
        The ID of this element.
        """
        return self._id

    @property
    def is_pending(self) -> bool:
        """
        Whether this element is pending execution.
        """
        return self._is_pending

    @property
    def task(self) -> app.WorkflowTask:
        """
        The task this is part of the enactment of.
        """
        return self._task

    @property
    def index(self) -> int:
        """Get the index of the element within the task.

        Note: the `global_idx` attribute returns the index of the element within the
        workflow, across all tasks."""

        return self._index

    @property
    def element_set_idx(self) -> int:
        """
        The index within the task of the element set containing this element.
        """
        return self._es_idx

    @property
    def element_set(self):
        """
        The element set containing this element.
        """
        return self.task.template.element_sets[self.element_set_idx]

    @property
    def sequence_idx(self) -> Dict[str, int]:
        """
        The sequence index IDs.
        """
        return self._seq_idx

    @property
    def input_source_idx(self) -> Dict[str, int]:
        """
        The input source indices.
        """
        return self._src_idx

    @property
    def input_sources(self) -> Dict[str, app.InputSource]:
        """
        The sources of the inputs to this element.
        """
        return {
            k: self.element_set.input_sources[k.split("inputs.")[1]][v]
            for k, v in self.input_source_idx.items()
        }

    @property
    def workflow(self) -> app.Workflow:
        """
        The workflow containing this element.
        """
        return self.task.workflow

    @property
    def iteration_IDs(self) -> List[int]:
        """
        The IDs of the iterations of this element.
        """
        return self._iteration_IDs

    @property
    @TimeIt.decorator
    def iterations(self) -> List[app.ElementIteration]:
        """
        The iterations of this element.
        """
        # TODO: fix this
        if self._iteration_objs is None:
            self._iteration_objs = [
                self.app.ElementIteration(
                    element=self,
                    index=idx,
                    **{k: v for k, v in iter_i.items() if k != "element_ID"},
                )
                for idx, iter_i in enumerate(self._iterations)
            ]
        return self._iteration_objs

    @property
    def dir_name(self):
        """
        The name of the directory for containing temporary files for this element.
        """
        return f"e_{self.index}"

    @property
    def latest_iteration(self):
        """
        The most recent iteration of this element.
        """
        return self.iterations[-1]

    @property
    def inputs(self) -> app.ElementInputs:
        """
        The inputs to this element (or its most recent iteration).
        """
        return self.latest_iteration.inputs

    @property
    def outputs(self) -> app.ElementOutputs:
        """
        The outputs from this element (or its most recent iteration).
        """
        return self.latest_iteration.outputs

    @property
    def input_files(self) -> app.ElementInputFiles:
        """
        The input files to this element (or its most recent iteration).
        """
        return self.latest_iteration.input_files

    @property
    def output_files(self) -> app.ElementOutputFiles:
        """
        The output files from this element (or its most recent iteration).
        """
        return self.latest_iteration.output_files

    @property
    def schema_parameters(self) -> List[str]:
        """
        The schema-defined parameters to this element (or its most recent iteration).
        """
        return self.latest_iteration.schema_parameters

    @property
    def actions(self) -> Dict[app.ElementAction]:
        """
        The actions of this element (or its most recent iteration).
        """
        return self.latest_iteration.actions

    @property
    def action_runs(self) -> List[app.ElementActionRun]:
        """
        A list of element action runs from the latest iteration, where only the
        final run is taken for each element action.
        """
        return self.latest_iteration.action_runs

    def init_loop_index(self, loop_name: str):
        """
        Initialise the loop index if necessary.
        """
        pass

    def to_element_set_data(self):
        """Generate lists of workflow-bound InputValues and ResourceList."""
        inputs = []
        resources = []
        for k, v in self.get_data_idx().items():
            k_s = k.split(".")

            if k_s[0] == "inputs":
                inp_val = self.app.InputValue(
                    parameter=k_s[1],
                    path=k_s[2:] or None,
                    value=None,
                )
                inp_val._value_group_idx = v
                inp_val._workflow = self.workflow
                inputs.append(inp_val)

            elif k_s[0] == "resources":
                scope = self.app.ActionScope.from_json_like(k_s[1])
                res = self.app.ResourceSpec(scope=scope)
                res._value_group_idx = v
                res._workflow = self.workflow
                resources.append(res)

        return inputs, resources

    def get_sequence_value(self, sequence_path: str) -> Any:
        """
        Get the value of a sequence that applies.
        """
        seq = self.element_set.get_sequence_from_path(sequence_path)
        if not seq:
            raise ValueError(
                f"No sequence with path {sequence_path!r} in this element's originating "
                f"element set."
            )
        return seq.values[self.sequence_idx[sequence_path]]

    def get_data_idx(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
    ) -> Dict[str, int]:
        """Get the data index of the most recent element iteration.

        Parameters
        ----------
        action_idx
            The index of the action within the schema.
        """
        return self.latest_iteration.get_data_idx(
            path=path,
            action_idx=action_idx,
            run_idx=run_idx,
        )

    def get_parameter_sources(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
        typ: str = None,
        as_strings: bool = False,
        use_task_index: bool = False,
    ) -> Dict[str, Union[str, Dict[str, Any]]]:
        """ "Get the parameter sources of the most recent element iteration.

        Parameters
        ----------
        use_task_index
            If True, use the task index within the workflow, rather than the task insert
            ID.
        """
        return self.latest_iteration.get_parameter_sources(
            path=path,
            action_idx=action_idx,
            run_idx=run_idx,
            typ=typ,
            as_strings=as_strings,
            use_task_index=use_task_index,
        )

    def get(
        self,
        path: str = None,
        action_idx: int = None,
        run_idx: int = -1,
        default: Any = None,
        raise_on_missing: bool = False,
        raise_on_unset: bool = False,
    ) -> Any:
        """Get element data of the most recent iteration from the persistent store."""
        return self.latest_iteration.get(
            path=path,
            action_idx=action_idx,
            run_idx=run_idx,
            default=default,
            raise_on_missing=raise_on_missing,
            raise_on_unset=raise_on_unset,
        )

    def get_EAR_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementActionRun]]:
        """Get EARs that the most recent iteration of this element depends on."""
        return self.latest_iteration.get_EAR_dependencies(as_objects=as_objects)

    def get_element_iteration_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementIteration]]:
        """Get element iterations that the most recent iteration of this element depends
        on."""
        return self.latest_iteration.get_element_iteration_dependencies(
            as_objects=as_objects
        )

    def get_element_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.Element]]:
        """Get elements that the most recent iteration of this element depends on."""
        return self.latest_iteration.get_element_dependencies(as_objects=as_objects)

    def get_input_dependencies(self) -> Dict[str, Dict]:
        """Get locally defined inputs/sequences/defaults from other tasks that this
        the most recent iteration of this element depends on."""
        return self.latest_iteration.get_input_dependencies()

    def get_task_dependencies(
        self, as_objects: bool = False
    ) -> List[Union[int, app.WorkflowTask]]:
        """Get tasks (insert ID or WorkflowTask objects) that the most recent iteration of
        this element depends on.

        Dependencies may come from either elements from upstream tasks, or from locally
        defined inputs/sequences/defaults from upstream tasks."""
        return self.latest_iteration.get_task_dependencies(as_objects=as_objects)

    def get_dependent_EARs(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementActionRun]]:
        """Get EARs that depend on the most recent iteration of this element."""
        return self.latest_iteration.get_dependent_EARs(as_objects=as_objects)

    def get_dependent_element_iterations(
        self, as_objects: bool = False
    ) -> List[Union[int, app.ElementIteration]]:
        """Get element iterations that depend on the most recent iteration of this
        element."""
        return self.latest_iteration.get_dependent_element_iterations(
            as_objects=as_objects
        )

    def get_dependent_elements(
        self, as_objects: bool = False
    ) -> List[Union[int, app.Element]]:
        """Get elements that depend on the most recent iteration of this element."""
        return self.latest_iteration.get_dependent_elements(as_objects=as_objects)

    def get_dependent_tasks(
        self, as_objects: bool = False
    ) -> List[Union[int, app.WorkflowTask]]:
        """Get tasks that depend on the most recent iteration of this element."""
        return self.latest_iteration.get_dependent_tasks(as_objects=as_objects)

    @TimeIt.decorator
    def get_dependent_elements_recursively(self, task_insert_ID=None):
        """Get downstream elements that depend on this element, including recursive
        dependencies.

        Dependencies are resolved using the initial iteration only. This method is used to
        identify from which element in the previous iteration a new iteration should be
        parametrised.

        Parameters
        ----------
        task_insert_ID
            If specified, only return elements from this task.

        """

        def get_deps(element):
            deps = element.iterations[0].get_dependent_elements(as_objects=False)
            deps_objs = self.workflow.get_elements_from_IDs(deps)
            return set(deps).union(
                [dep_j for deps_i in deps_objs for dep_j in get_deps(deps_i)]
            )

        all_deps = get_deps(self)

        if task_insert_ID is not None:
            elem_ID_subset = self.workflow.tasks.get(insert_ID=task_insert_ID).element_IDs
            all_deps = [i for i in all_deps if i in elem_ID_subset]

        return self.workflow.get_elements_from_IDs(sorted(all_deps))


@dataclass
class ElementParameter:
    """
    A parameter to an :py:class:`.Element`.

    Parameters
    ----------
    task: ~hpcflow.app.WorkflowTask
        The task that this is part of.
    path: str
        The path to this parameter.
    parent: Element | ~hpcflow.app.ElementAction | ~hpcflow.app.ElementActionRun | ~hpcflow.app.Parameters
        The entity that owns this parameter.
    element: Element
        The element that this is a parameter of.
    """

    _app_attr = "app"

    #: The task that this is part of.
    task: app.WorkflowTask
    #: The path to this parameter.
    path: str
    #: The entity that owns this parameter.
    parent: Union[Element, app.ElementAction, app.ElementActionRun, app.Parameters]
    #: The element that this is a parameter of.
    element: Element

    @property
    def data_idx(self):
        """
        The data indices associated with this parameter.
        """
        return self.parent.get_data_idx(path=self.path)

    @property
    def value(self) -> Any:
        """
        The value of this parameter.
        """
        return self.parent.get(path=self.path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(element={self.element!r}, path={self.path!r})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False
        if self.task == __o.task and self.path == __o.path:
            return True

    @property
    def data_idx_is_set(self):
        """
        The associated data indices for which this is set.
        """
        return {
            k: self.task.workflow.is_parameter_set(v) for k, v in self.data_idx.items()
        }

    @property
    def is_set(self):
        """
        Whether this parameter is set.
        """
        return all(self.data_idx_is_set.values())

    def get_size(self, **store_kwargs):
        """
        Get the size of the parameter.
        """
        raise NotImplementedError


@dataclass
class ElementFilter(JSONLike):
    """
    A filter for iterations.

    Parameters
    ----------
    rules: list[~hpcflow.app.Rule]
        The filtering rules to use.
    """

    _child_objects = (ChildObjectSpec(name="rules", is_multiple=True, class_name="Rule"),)

    #: The filtering rules to use.
    rules: List[app.Rule] = field(default_factory=list)

    def filter(
        self, element_iters: List[app.ElementIteration]
    ) -> List[app.ElementIteration]:
        """
        Apply the filter rules to select a subsequence of iterations.
        """
        out = []
        for i in element_iters:
            if all(rule_j.test(i) for rule_j in self.rules):
                out.append(i)
        return out


@dataclass
class ElementGroup(JSONLike):
    """
    A grouping rule for element iterations.

    Parameters
    ----------
    name:
        The name of the grouping rule.
    where:
        A filtering rule to select which iterations to use in the group.
    group_by_distinct:
        If specified, the name of the property to group iterations by.
    """

    #: The name of the grouping rule.
    name: str
    #: A filtering rule to select which iterations to use in the group.
    where: Optional[ElementFilter] = None
    #: If specified, the name of the property to group iterations by.
    group_by_distinct: Optional[app.ParameterPath] = None

    def __post_init__(self):
        self.name = check_valid_py_identifier(self.name)


@dataclass
class ElementRepeats:
    """
    A repetition rule.

    Parameters
    ----------
    number:
        The number of times to repeat.
    where:
        A filtering rule for what to repeat.
    """

    #: The number of times to repeat.
    number: int
    #: A filtering rule for what to repeat.
    where: Optional[ElementFilter] = None
