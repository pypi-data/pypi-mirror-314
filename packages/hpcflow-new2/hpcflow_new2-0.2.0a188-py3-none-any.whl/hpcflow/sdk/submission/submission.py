"""
A collection of submissions to a scheduler, generated from a workflow.
"""

from __future__ import annotations
from collections import defaultdict

from datetime import datetime, timedelta, timezone
import enum
import os
from pathlib import Path
from textwrap import indent
from typing import Dict, List, Optional, Tuple

from hpcflow.sdk import app
from hpcflow.sdk.core.element import ElementResources
from hpcflow.sdk.core.errors import (
    JobscriptSubmissionFailure,
    MissingEnvironmentError,
    MissingEnvironmentExecutableError,
    MissingEnvironmentExecutableInstanceError,
    MultipleEnvironmentsError,
    SubmissionFailure,
)
from hpcflow.sdk.core.json_like import ChildObjectSpec, JSONLike
from hpcflow.sdk.core.object_list import ObjectListMultipleMatchError
from hpcflow.sdk.log import TimeIt


def timedelta_format(td: timedelta) -> str:
    """
    Convert time delta to string in standard form.
    """
    days, seconds = td.days, td.seconds
    hours = seconds // (60 * 60)
    seconds -= hours * (60 * 60)
    minutes = seconds // 60
    seconds -= minutes * 60
    return f"{days}-{hours:02}:{minutes:02}:{seconds:02}"


def timedelta_parse(td_str: str) -> timedelta:
    """
    Parse a string in standard form as a time delta.
    """
    days, other = td_str.split("-")
    days = int(days)
    hours, mins, secs = [int(i) for i in other.split(":")]
    return timedelta(days=days, hours=hours, minutes=mins, seconds=secs)


class SubmissionStatus(enum.Enum):
    """
    The overall status of a submission.
    """

    #: Not yet submitted.
    PENDING = 0
    #: All jobscripts submitted successfully.
    SUBMITTED = 1
    #: Some jobscripts submitted successfully.
    PARTIALLY_SUBMITTED = 2


class Submission(JSONLike):
    """
    A collection of jobscripts to be submitted to a scheduler.

    Parameters
    ----------
    index: int
        The index of this submission.
    jobscripts: list[~hpcflow.app.Jobscript]
        The jobscripts in the submission.
    workflow: ~hpcflow.app.Workflow
        The workflow this is part of.
    submission_parts: dict
        Description of submission parts.
    JS_parallelism: bool
        Whether to exploit jobscript parallelism.
    environments: ~hpcflow.app.EnvironmentsList
        The execution environments to use.
    """

    _child_objects = (
        ChildObjectSpec(
            name="jobscripts",
            class_name="Jobscript",
            is_multiple=True,
            parent_ref="_submission",
        ),
        ChildObjectSpec(
            name="environments",
            class_name="EnvironmentsList",
        ),
    )

    def __init__(
        self,
        index: int,
        jobscripts: List[app.Jobscript],
        workflow: Optional[app.Workflow] = None,
        submission_parts: Optional[Dict] = None,
        JS_parallelism: Optional[bool] = None,
        environments: Optional[app.EnvironmentsList] = None,
    ):
        self._index = index
        self._jobscripts = jobscripts
        self._submission_parts = submission_parts or {}
        self._JS_parallelism = JS_parallelism
        self._environments = environments

        self._submission_parts_lst = None  # assigned on first access; datetime objects

        if workflow:
            #: The workflow this is part of.
            self.workflow = workflow

        self._set_parent_refs()

        for js_idx, js in enumerate(self.jobscripts):
            js._index = js_idx

    @TimeIt.decorator
    def _set_environments(self):
        filterable = ElementResources.get_env_instance_filterable_attributes()

        # map required environments and executable labels to job script indices:
        req_envs = defaultdict(lambda: defaultdict(set))
        for js_idx, js_i in enumerate(self.jobscripts):
            for run in js_i.all_EARs:
                env_spec_h = tuple(zip(*run.env_spec.items()))  # hashable
                for exec_label_j in run.action.get_required_executables():
                    req_envs[env_spec_h][exec_label_j].add(js_idx)
                if env_spec_h not in req_envs:
                    req_envs[env_spec_h] = {}

        # check these envs/execs exist in app data:
        envs = []
        for env_spec_h, exec_js in req_envs.items():
            env_spec = dict(zip(*env_spec_h))
            non_name_spec = {k: v for k, v in env_spec.items() if k != "name"}
            spec_str = f" with specifiers {non_name_spec!r}" if non_name_spec else ""
            env_ref = f"{env_spec['name']!r}{spec_str}"
            try:
                env_i = self.app.envs.get(**env_spec)
            except ObjectListMultipleMatchError:
                raise MultipleEnvironmentsError(
                    f"Multiple environments {env_ref} are defined on this machine."
                )
            except ValueError:
                raise MissingEnvironmentError(
                    f"The environment {env_ref} is not defined on this machine, so the "
                    f"submission cannot be created."
                ) from None
            else:
                if env_i not in envs:
                    envs.append(env_i)

            for exec_i_lab, js_idx_set in exec_js.items():
                try:
                    exec_i = env_i.executables.get(exec_i_lab)
                except ValueError:
                    raise MissingEnvironmentExecutableError(
                        f"The environment {env_ref} as defined on this machine has no "
                        f"executable labelled {exec_i_lab!r}, which is required for this "
                        f"submission, so the submission cannot be created."
                    ) from None

                # check matching executable instances exist:
                for js_idx_j in js_idx_set:
                    js_j = self.jobscripts[js_idx_j]
                    filter_exec = {j: getattr(js_j.resources, j) for j in filterable}
                    exec_instances = exec_i.filter_instances(**filter_exec)
                    if not exec_instances:
                        raise MissingEnvironmentExecutableInstanceError(
                            f"No matching executable instances found for executable "
                            f"{exec_i_lab!r} of environment {env_ref} for jobscript "
                            f"index {js_idx_j!r} with requested resources "
                            f"{filter_exec!r}."
                        )

        # save env definitions to the environments attribute:
        self._environments = self.app.EnvironmentsList(envs)

    def to_dict(self):
        dct = super().to_dict()
        del dct["_workflow"]
        del dct["_index"]
        del dct["_submission_parts_lst"]
        dct = {k.lstrip("_"): v for k, v in dct.items()}
        return dct

    @property
    def index(self) -> int:
        """
        The index of this submission.
        """
        return self._index

    @property
    def environments(self) -> app.EnvironmentsList:
        """
        The execution environments to use.
        """
        return self._environments

    @property
    def submission_parts(self) -> List[Dict]:
        """
        Description of the parts of this submission.
        """
        if not self._submission_parts:
            return []

        if self._submission_parts_lst is None:
            self._submission_parts_lst = [
                {
                    "submit_time": datetime.strptime(dt, self.workflow.ts_fmt)
                    .replace(tzinfo=timezone.utc)
                    .astimezone(),
                    "jobscripts": js_idx,
                }
                for dt, js_idx in self._submission_parts.items()
            ]
        return self._submission_parts_lst

    @TimeIt.decorator
    def get_start_time(self, submit_time: str) -> Union[datetime, None]:
        """Get the start time of a given submission part."""
        js_idx = self._submission_parts[submit_time]
        all_part_starts = []
        for i in js_idx:
            start_time = self.jobscripts[i].start_time
            if start_time:
                all_part_starts.append(start_time)
        if all_part_starts:
            return min(all_part_starts)
        else:
            return None

    @TimeIt.decorator
    def get_end_time(self, submit_time: str) -> Union[datetime, None]:
        """Get the end time of a given submission part."""
        js_idx = self._submission_parts[submit_time]
        all_part_ends = []
        for i in js_idx:
            end_time = self.jobscripts[i].end_time
            if end_time:
                all_part_ends.append(end_time)
        if all_part_ends:
            return max(all_part_ends)
        else:
            return None

    @property
    @TimeIt.decorator
    def start_time(self):
        """Get the first non-None start time over all submission parts."""
        all_start_times = []
        for submit_time in self._submission_parts:
            start_i = self.get_start_time(submit_time)
            if start_i:
                all_start_times.append(start_i)
        if all_start_times:
            return max(all_start_times)
        else:
            return None

    @property
    @TimeIt.decorator
    def end_time(self):
        """Get the final non-None end time over all submission parts."""
        all_end_times = []
        for submit_time in self._submission_parts:
            end_i = self.get_end_time(submit_time)
            if end_i:
                all_end_times.append(end_i)
        if all_end_times:
            return max(all_end_times)
        else:
            return None

    @property
    def jobscripts(self) -> List:
        """
        The jobscripts in this submission.
        """
        return self._jobscripts

    @property
    def JS_parallelism(self):
        """
        Whether to exploit jobscript parallelism.
        """
        return self._JS_parallelism

    @property
    def workflow(self) -> List:
        """
        The workflow this is part of.
        """
        return self._workflow

    @workflow.setter
    def workflow(self, wk):
        self._workflow = wk

    @property
    def jobscript_indices(self) -> Tuple[int]:
        """All associated jobscript indices."""
        return tuple(i.index for i in self.jobscripts)

    @property
    def submitted_jobscripts(self) -> Tuple[int]:
        """Jobscript indices that have been successfully submitted."""
        return tuple(j for i in self.submission_parts for j in i["jobscripts"])

    @property
    def outstanding_jobscripts(self) -> Tuple[int]:
        """Jobscript indices that have not yet been successfully submitted."""
        return tuple(set(self.jobscript_indices) - set(self.submitted_jobscripts))

    @property
    def status(self):
        """
        The status of this submission.
        """
        if not self.submission_parts:
            return SubmissionStatus.PENDING
        else:
            if set(self.submitted_jobscripts) == set(self.jobscript_indices):
                return SubmissionStatus.SUBMITTED
            else:
                return SubmissionStatus.PARTIALLY_SUBMITTED

    @property
    def needs_submit(self):
        """
        Whether this submission needs a submit to be done.
        """
        return self.status in (
            SubmissionStatus.PENDING,
            SubmissionStatus.PARTIALLY_SUBMITTED,
        )

    @property
    def path(self):
        """
        The path to files associated with this submission.
        """
        return self.workflow.submissions_path / str(self.index)

    @property
    def all_EAR_IDs(self):
        """
        The IDs of all EARs in this submission.
        """
        return [i for js in self.jobscripts for i in js.all_EAR_IDs]

    @property
    def all_EARs(self):
        """
        All EARs in this this submission.
        """
        return [i for js in self.jobscripts for i in js.all_EARs]

    @property
    @TimeIt.decorator
    def EARs_by_elements(self):
        """
        All EARs in this submission, grouped by element.
        """
        task_elem_EARs = defaultdict(lambda: defaultdict(list))
        for i in self.all_EARs:
            task_elem_EARs[i.task.index][i.element.index].append(i)
        return task_elem_EARs

    @property
    def abort_EARs_file_name(self):
        """
        The name of a file describing what EARs have aborted.
        """
        return f"abort_EARs.txt"

    @property
    def abort_EARs_file_path(self):
        """
        The path to the file describing what EARs have aborted in this submission.
        """
        return self.path / self.abort_EARs_file_name

    @TimeIt.decorator
    def get_active_jobscripts(
        self, as_json: bool = False
    ) -> List[Tuple[int, Dict[int, JobscriptElementState]]]:
        """Get jobscripts that are active on this machine, and their active states."""
        # this returns: {JS_IDX: {JS_ELEMENT_IDX: STATE}}
        # TODO: query the scheduler once for all jobscripts?
        out = {}
        for js in self.jobscripts:
            active_states = js.get_active_states(as_json=as_json)
            if active_states:
                out[js.index] = active_states
        return out

    def _write_abort_EARs_file(self):
        with self.abort_EARs_file_path.open(mode="wt", newline="\n") as fp:
            # write a single line for each EAR currently in the workflow:
            fp.write("\n".join("0" for _ in range(self.workflow.num_EARs)) + "\n")

    def _set_run_abort(self, run_ID: int):
        """Modify the abort runs file to indicate a specified run should be aborted."""
        with self.abort_EARs_file_path.open(mode="rt", newline="\n") as fp:
            lines = fp.read().splitlines()
        lines[run_ID] = "1"

        # write a new temporary run-abort file:
        tmp_suffix = self.abort_EARs_file_path.suffix + ".tmp"
        tmp = self.abort_EARs_file_path.with_suffix(tmp_suffix)
        self.app.submission_logger.debug(f"Creating temporary run abort file: {tmp!r}.")
        with tmp.open(mode="wt", newline="\n") as fp:
            fp.write("\n".join(i for i in lines) + "\n")

        # atomic rename, overwriting original:
        self.app.submission_logger.debug(
            "Replacing original run abort file with new temporary file."
        )
        os.replace(src=tmp, dst=self.abort_EARs_file_path)

    @staticmethod
    def get_unique_schedulers_of_jobscripts(
        jobscripts: List[Jobscript],
    ) -> Dict[Tuple[Tuple[int, int]], Scheduler]:
        """Get unique schedulers and which of the passed jobscripts they correspond to.

        Uniqueness is determines only by the `Scheduler.unique_properties` tuple.

        Parameters
        ----------
        jobscripts: list[~hpcflow.app.Jobscript]
        """
        js_idx = []
        schedulers = []

        # list of tuples of scheduler properties we consider to determine "uniqueness",
        # with the first string being the scheduler type (class name):
        seen_schedulers = []

        for js in jobscripts:
            if js.scheduler.unique_properties not in seen_schedulers:
                seen_schedulers.append(js.scheduler.unique_properties)
                schedulers.append(js.scheduler)
                js_idx.append([])
            sched_idx = seen_schedulers.index(js.scheduler.unique_properties)
            js_idx[sched_idx].append((js.submission.index, js.index))

        sched_js_idx = dict(zip((tuple(i) for i in js_idx), schedulers))

        return sched_js_idx

    @TimeIt.decorator
    def get_unique_schedulers(self) -> Dict[Tuple[int], Scheduler]:
        """Get unique schedulers and which of this submission's jobscripts they
        correspond to."""
        return self.get_unique_schedulers_of_jobscripts(self.jobscripts)

    @TimeIt.decorator
    def get_unique_shells(self) -> Dict[Tuple[int], Shell]:
        """Get unique shells and which jobscripts they correspond to."""
        js_idx = []
        shells = []

        for js in self.jobscripts:
            if js.shell not in shells:
                shells.append(js.shell)
                js_idx.append([])
            shell_idx = shells.index(js.shell)
            js_idx[shell_idx].append(js.index)

        shell_js_idx = dict(zip((tuple(i) for i in js_idx), shells))

        return shell_js_idx

    def _raise_failure(self, submitted_js_idx, exceptions):
        msg = f"Some jobscripts in submission index {self.index} could not be submitted"
        if submitted_js_idx:
            msg += f" (but jobscripts {submitted_js_idx} were submitted successfully):"
        else:
            msg += ":"

        msg += "\n"
        for sub_err in exceptions:
            msg += (
                f"Jobscript {sub_err.js_idx} at path: {str(sub_err.js_path)!r}\n"
                f"Submit command: {sub_err.submit_cmd!r}.\n"
                f"Reason: {sub_err.message!r}\n"
            )
            if sub_err.subprocess_exc is not None:
                msg += f"Subprocess exception: {sub_err.subprocess_exc}\n"
            if sub_err.job_ID_parse_exc is not None:
                msg += f"Subprocess job ID parse exception: {sub_err.job_ID_parse_exc}\n"
            if sub_err.job_ID_parse_exc is not None:
                msg += f"Job ID parse exception: {sub_err.job_ID_parse_exc}\n"
            if sub_err.stdout:
                msg += f"Submission stdout:\n{indent(sub_err.stdout, '  ')}\n"
            if sub_err.stderr:
                msg += f"Submission stderr:\n{indent(sub_err.stderr, '  ')}\n"

        raise SubmissionFailure(message=msg)

    def _append_submission_part(self, submit_time: str, submitted_js_idx: List[int]):
        self._submission_parts[submit_time] = submitted_js_idx
        self.workflow._store.add_submission_part(
            sub_idx=self.index,
            dt_str=submit_time,
            submitted_js_idx=submitted_js_idx,
        )

    @TimeIt.decorator
    def submit(
        self,
        status,
        ignore_errors: Optional[bool] = False,
        print_stdout: Optional[bool] = False,
        add_to_known: Optional[bool] = True,
    ) -> List[int]:
        """Generate and submit the jobscripts of this submission."""

        # if JS_parallelism explicitly requested but store doesn't support, raise:
        supports_JS_para = self.workflow._store._features.jobscript_parallelism
        if self.JS_parallelism:
            if not supports_JS_para:
                if status:
                    status.stop()
                raise ValueError(
                    f"Store type {self.workflow._store!r} does not support jobscript "
                    f"parallelism."
                )
        elif self.JS_parallelism is None:
            self._JS_parallelism = supports_JS_para

        # set os_name and shell_name for each jobscript:
        for js in self.jobscripts:
            js._set_os_name()
            js._set_shell_name()
            js._set_scheduler_name()

        outstanding = self.outstanding_jobscripts

        # get scheduler, shell and OS version information (also an opportunity to fail
        # before trying to submit jobscripts):
        js_vers_info = {}
        for js_indices, sched in self.get_unique_schedulers().items():
            try:
                vers_info = sched.get_version_info()
            except Exception as err:
                if ignore_errors:
                    vers_info = {}
                else:
                    raise err
            for _, js_idx in js_indices:
                if js_idx in outstanding:
                    if js_idx not in js_vers_info:
                        js_vers_info[js_idx] = {}
                    js_vers_info[js_idx].update(vers_info)

        for js_indices, shell in self.get_unique_shells().items():
            try:
                vers_info = shell.get_version_info()
            except Exception as err:
                if ignore_errors:
                    vers_info = {}
                else:
                    raise err
            for js_idx in js_indices:
                if js_idx in outstanding:
                    if js_idx not in js_vers_info:
                        js_vers_info[js_idx] = {}
                    js_vers_info[js_idx].update(vers_info)

        for js_idx, vers_info_i in js_vers_info.items():
            self.jobscripts[js_idx]._set_version_info(vers_info_i)

        # for direct submission, it's important that os_name/shell_name/scheduler_name
        # are made persistent now, because `Workflow.write_commands`, which might be
        # invoked in a new process before submission has completed, needs to know these:
        self.workflow._store._pending.commit_all()

        # TODO: a submission should only be "submitted" once shouldn't it?
        # no; there could be an IO error (e.g. internet connectivity), so might
        # need to be able to reattempt submission of outstanding jobscripts.
        self.path.mkdir(exist_ok=True)
        if not self.abort_EARs_file_path.is_file():
            self._write_abort_EARs_file()

        # map jobscript `index` to (scheduler job ID or process ID, is_array):
        scheduler_refs = {}
        submitted_js_idx = []
        errs = []
        for js in self.jobscripts:
            # check not previously submitted:
            if js.index not in outstanding:
                continue

            # check all dependencies were submitted now or previously:
            if not all(
                i in submitted_js_idx or i in self.submitted_jobscripts
                for i in js.dependencies
            ):
                continue

            try:
                if status:
                    status.update(f"Submitting jobscript {js.index}...")
                js_ref_i = js.submit(scheduler_refs, print_stdout=print_stdout)
                scheduler_refs[js.index] = (js_ref_i, js.is_array)
                submitted_js_idx.append(js.index)

            except JobscriptSubmissionFailure as err:
                errs.append(err)
                continue

        if submitted_js_idx:
            dt_str = datetime.utcnow().strftime(self.app._submission_ts_fmt)
            self._append_submission_part(
                submit_time=dt_str,
                submitted_js_idx=submitted_js_idx,
            )
            # add a record of the submission part to the known-submissions file
            if add_to_known:
                self.app._add_to_known_submissions(
                    wk_path=self.workflow.path,
                    wk_id=self.workflow.id_,
                    sub_idx=self.index,
                    sub_time=dt_str,
                )

        if errs and not ignore_errors:
            if status:
                status.stop()
            self._raise_failure(submitted_js_idx, errs)

        len_js = len(submitted_js_idx)
        print(f"Submitted {len_js} jobscript{'s' if len_js > 1 else ''}.")

        return submitted_js_idx

    @TimeIt.decorator
    def cancel(self):
        """
        Cancel the active jobs for this submission's jobscripts.
        """
        act_js = list(self.get_active_jobscripts())
        if not act_js:
            print("No active jobscripts to cancel.")
            return
        for js_indices, sched in self.get_unique_schedulers().items():
            # filter by active jobscripts:
            js_idx = [i[1] for i in js_indices if i[1] in act_js]
            if js_idx:
                print(
                    f"Cancelling jobscripts {js_idx!r} of submission {self.index} of "
                    f"workflow {self.workflow.name!r}."
                )
                jobscripts = [self.jobscripts[i] for i in js_idx]
                sched_refs = [i.scheduler_js_ref for i in jobscripts]
                sched.cancel_jobs(js_refs=sched_refs, jobscripts=jobscripts)
            else:
                print("No active jobscripts to cancel.")
