import os
import sys
from importlib import metadata
import pathlib
main_dir = 'my_main_dir'
sub_dir = 'sub_dir'
fname = 'filename.tsv'


LAB_PROJECT_NAME = 'lab-partner'
LAB_CICD_ARTIFACT_STORAGE = '/opt/lab/cicd/artifacts'
LAB_CICD_ARTIFACT_STORAGE_HOST_PATH = '/tmp/lab-cicd'


def project_name() -> str:
    return LAB_PROJECT_NAME


def version() -> str:
    return metadata.version(LAB_PROJECT_NAME)


def workspace() -> str:
    return os.environ['LAB_WORKSPACE']


def workspace_data() -> str:
    return str(pathlib.Path(workspace(), ''))


def cicd_storage_path() -> str:
    return LAB_CICD_ARTIFACT_STORAGE


def cicd_storage_path_host_path() -> str:
    return LAB_CICD_ARTIFACT_STORAGE_HOST_PATH


def is_linux() -> bool:
    """
    Check current platform is Linux
    :return: True on Linux
    """
    return sys.platform in ('linux',)


def is_supported_platform() -> bool:
    """
    Check current platform is MacOS or Linux
    :return: True on MacOS or Linux
    """
    return sys.platform in ('darwin', 'linux')


def lab_role_label():
    return 'lab-role'


def lab_container_runtime_role():
    return 'container-runtime'


def lab_shell_role():
    return 'shell'


def lab_network_name():
    return 'lab'
