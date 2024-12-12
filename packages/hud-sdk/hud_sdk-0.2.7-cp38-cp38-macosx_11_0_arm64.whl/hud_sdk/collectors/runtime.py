import os
import platform
import sys
from typing import List

from ..process_utils import get_current_pid
from ..schemas.events import Runtime


def get_python_version() -> str:
    return sys.version


def get_platform_info() -> str:
    return platform.platform()


def get_architecture() -> str:
    return platform.architecture()[0]


def get_cwd() -> str:
    return os.getcwd()


def get_exec_path() -> str:
    return sys.executable


def get_argv() -> List[str]:
    return sys.argv


def runtime_info() -> Runtime:
    return Runtime(
        python_version=get_python_version(),
        platform_info=get_platform_info(),
        architecture=get_architecture(),
        pid=get_current_pid(),
        cwd=get_cwd(),
        exec_path=get_exec_path(),
        argv=get_argv(),
    )
