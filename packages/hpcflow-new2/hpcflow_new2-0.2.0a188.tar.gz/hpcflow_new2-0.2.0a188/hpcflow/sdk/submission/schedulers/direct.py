"""
A direct job "scheduler" that just runs immediate subprocesses.
"""

from pathlib import Path
import shutil
import signal
from typing import Callable, Dict, List, Optional, Tuple

import psutil
from hpcflow.sdk.submission.jobscript_info import JobscriptElementState

from hpcflow.sdk.submission.schedulers import NullScheduler
from hpcflow.sdk.submission.shells.base import Shell


class DirectScheduler(NullScheduler):
    """
    A direct scheduler, that just runs jobs immediately as direct subprocesses.

    The correct subclass (:py:class:`DirectPosix` or :py:class:`DirectWindows`) should
    be used to create actual instances.

    Keyword Args
    ------------
    shell_args: str
        Arguments to pass to the shell. Pre-quoted.
    shebang_args: str
        Arguments to set on the shebang line. Pre-quoted.
    options: dict
        Options to the jobscript command.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def process_resources(cls, resources, scheduler_config: Dict) -> None:
        """Perform scheduler-specific processing to the element resources.

        Note: this mutates `resources`.

        """
        return

    def get_submit_command(
        self,
        shell: Shell,
        js_path: str,
        deps: List[Tuple],
    ) -> List[str]:
        """
        Get the concrete submission command.
        """
        return shell.get_direct_submit_command(js_path)

    @staticmethod
    def _kill_processes(
        procs: List[psutil.Process],
        sig=signal.SIGTERM,
        timeout=None,
        on_terminate=None,
    ):
        all_procs = []
        for i in procs:
            all_procs.append(i)
            all_procs.extend(i.children(recursive=True))

        for i in all_procs:
            try:
                i.send_signal(sig)
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(all_procs, timeout=timeout, callback=on_terminate)
        for p in alive:
            p.kill()

    @staticmethod
    def _get_jobscript_processes(js_refs: List[Tuple[int, List[str]]]):
        procs = []
        for p_id, p_cmdline in js_refs:
            try:
                proc_i = psutil.Process(p_id)
            except psutil.NoSuchProcess:
                # process might have completed already
                continue
            if proc_i.cmdline() == p_cmdline:
                # additional check this is the same process that we submitted
                procs.append(proc_i)
        return procs

    @classmethod
    def wait_for_jobscripts(
        cls,
        js_refs: List[Tuple[int, List[str]]],
        callback: Optional[Callable] = None,
    ) -> None:
        """Wait until the specified jobscripts have completed."""
        procs = cls._get_jobscript_processes(js_refs)
        (gone, alive) = psutil.wait_procs(procs, callback=callback)
        assert not alive
        return gone

    def get_job_state_info(
        self,
        js_refs: List[Tuple[int, List[str]]],
        num_js_elements: int,
    ) -> Dict[int, Dict[int, JobscriptElementState]]:
        """Query the scheduler to get the states of all of this user's jobs, optionally
        filtering by specified job IDs.

        Jobs that are not in the scheduler's status output will not appear in the output
        of this method."""
        info = {}
        for p_id, p_cmdline in js_refs:
            is_active = self.is_jobscript_active(p_id, p_cmdline)
            if is_active:
                # as far as the "scheduler" is concerned, all elements are running:
                info[p_id] = {
                    i: JobscriptElementState.running for i in range(num_js_elements)
                }

        return info

    def cancel_jobs(
        self,
        js_refs: List[Tuple[int, List[str]]],
        jobscripts: List = None,
    ):
        """
        Cancel some jobs.
        """

        def callback(proc):
            try:
                js = js_proc_id[proc.pid]
            except KeyError:
                # child process of one of the jobscripts
                self.app.submission_logger.debug(
                    f"jobscript child process ({proc.pid}) killed"
                )
                return
            print(
                f"Jobscript {js.index} from submission {js.submission.index} "
                f"terminated (user-initiated cancel) with exit code {proc.returncode}."
            )

        procs = self._get_jobscript_processes(js_refs)
        self.app.submission_logger.info(
            f"cancelling {self.__class__.__name__} jobscript processes: {procs}."
        )
        js_proc_id = {i.pid: jobscripts[idx] for idx, i in enumerate(procs)}
        self._kill_processes(procs, timeout=3, on_terminate=callback)
        self.app.submission_logger.info(f"jobscripts cancel command executed.")

    def is_jobscript_active(self, process_ID: int, process_cmdline: List[str]):
        """Query if a jobscript is running.

        Note that a "running" jobscript might be waiting on upstream jobscripts to
        complete.

        """
        try:
            proc = psutil.Process(process_ID)
        except psutil.NoSuchProcess:
            return False

        if proc.cmdline() == process_cmdline:
            return True
        else:
            return False


class DirectPosix(DirectScheduler):
    """
    A direct scheduler for POSIX systems.

    Keyword Args
    ------------
    shell_args: str
        Arguments to pass to the shell. Pre-quoted.
    shebang_args: str
        Arguments to set on the shebang line. Pre-quoted.
    options: dict
        Options to the jobscript command.
    """

    _app_attr = "app"
    #: Default shell.
    DEFAULT_SHELL_EXECUTABLE = "/bin/bash"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DirectWindows(DirectScheduler):
    """
    A direct scheduler for Windows.

    Keyword Args
    ------------
    shell_args: str
        Arguments to pass to the shell. Pre-quoted.
    options: dict
        Options to the jobscript command.
    """

    _app_attr = "app"
    #: Default shell.
    DEFAULT_SHELL_EXECUTABLE = "powershell.exe"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_submit_command(
        self, shell: Shell, js_path: str, deps: List[Tuple]
    ) -> List[str]:
        cmd = super().get_submit_command(shell, js_path, deps)
        # `Start-Process` (see `Jobscript._launch_direct_js_win`) seems to resolve the
        # executable, which means the process's `cmdline` might look different to what we
        # record; so let's resolve it ourselves:
        cmd[0] = shutil.which(cmd[0])
        return cmd
