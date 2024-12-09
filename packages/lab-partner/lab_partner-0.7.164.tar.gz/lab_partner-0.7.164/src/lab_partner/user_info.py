import os
import grp
from typing import Optional
import logging


logger = logging.getLogger(__name__)


def home() -> str:
    """Home directory of the current user

    :return: path to home directory
    """
    return os.environ['HOME']

def username() -> str:
    """Name of the current user

    :return: current user name
    """
    return os.environ['USER']

def user_runtime_tmp_path() -> str:
    return os.environ['XDG_RUNTIME_DIR']

def uid() -> int:
    """UID of the current user

    :return: current user UID
    """
    return os.getuid()

def gid() -> int:
    """GID of the current user

    :return: current user GID
    """
    return os.getgid()

def docker_gid() -> Optional[int]:
    try:
        return grp.getgrnam('docker').gr_gid
    except KeyError:
        logger.debug('Group "docker" does not exist')


def home_subdir(subdir: str) -> str:
    """
    Returns the path to a subdirectory under the user's home directory on the host system.
    :param subdir: Subdirectory (e.g. ".ssh")
    :return: Absolute path to home sub
    """
    return os.path.join(home(), subdir)