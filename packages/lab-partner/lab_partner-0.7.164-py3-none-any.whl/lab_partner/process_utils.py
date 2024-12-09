import logging
import sys
import os
import shlex
from subprocess import (
    Popen,
    PIPE,
    STDOUT,
    CalledProcessError,
    check_call,
    DEVNULL
)
import json
from typing import Iterable, Dict, Any, List, Optional

from .types import ShellCommand


logger = logging.getLogger(__name__)


def run_process_quiet(command: ShellCommand, env: Optional[Dict[str, str]] = None):
    command_parts = shlex.split(command) if isinstance(command, str) else command
    check_call(command_parts, stdout=DEVNULL, stderr=DEVNULL, env=env)


def run_process_stream_result(command: ShellCommand, env: Optional[Dict[str, str]] = None) -> Iterable[str]:
    """Run subprocess that redirects stderr to stdout to support applications
    that use stderr to separate logs types rather than just signalling error.

    :param command: the command line string to be executed
    :return: a generator of each returned line from STDOUT
    """
    command_parts = shlex.split(command) if isinstance(command, str) else command
    with Popen(command_parts, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True, env=env, encoding='utf-8') as p:
        if p.stdout:
            for line in p.stdout:
                if line:
                    yield line
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)


def process_output_as_json(process_output: Iterable[str]) -> List[Dict[str, Any]]:
    """Convert the results of a subprocess to a json generator

    :param process_output: output from running `run_process(...)`
    :return:
    """
    return [json.loads(output) for output in process_output]


def run_process(command: ShellCommand, env: Optional[Dict[str, str]] = None) -> List[str]:
    return list(run_process_stream_result(command, env))


def run_process_single_result(command: ShellCommand, env: Optional[Dict[str, str]] = None) -> str:
    return run_process(command, env)[0]


def exec_process(command: ShellCommand, env: Optional[Dict[str, str]] = None) -> None:
    """
    Exec a  process by forking the current process allowing the child
    to take over the main process id

    :param command: any command line string to execute
    :param input: text content to send to STDIN of the process
    """
    command_parts = shlex.split(command) if isinstance(command, str) else command
    if env:
        os.execvpe(command_parts[0], command_parts, env)
    else:
        os.execvp(command_parts[0], command_parts)


def exec_process_with_input(command: str, input: str, env: Optional[Dict[str, str]] = None) -> None:
    """
    Exec a  process by forking the current process allowing the child
    to take over the main process id

    :param command: any command line string to execute
    :param input: text content to send to STDIN of the process
    """
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Child process
        os.dup2(r, sys.stdin.fileno())
        os.close(r)
        os.close(w)
        command_parts = shlex.split(command)
        if env:
            os.execvpe(command_parts[0], command_parts, env)
        else:
            os.execvp(command_parts[0], command_parts)
    else:
        # Parent process
        os.close(r)
        os.write(w, bytearray(input, 'utf-8'))
        os.close(w)
        pid, status = os.waitpid(pid, 0)
