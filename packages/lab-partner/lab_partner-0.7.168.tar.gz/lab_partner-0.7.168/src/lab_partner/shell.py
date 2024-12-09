import logging
from lab_partner.docker import DockerComposeClient, DockerEnvironment, LabelFilter
from . import config


logger = logging.getLogger(__name__)


LAB_SHELL_CONTAINER_NAME = 'lab-shell'
LAB_SHELL_COMPOSE_CONFIG_PATH = 'lab_partner.compose_config.shell'


class ShellContainer:
    def __init__(self, env: DockerEnvironment):
        self._container_name = LAB_SHELL_CONTAINER_NAME
        self._docker_client = DockerComposeClient(config.project_name(), LAB_SHELL_COMPOSE_CONFIG_PATH, env)
        self._role_label_filter = LabelFilter(config.lab_role_label(), config.lab_shell_role())

    def start(self) -> None:
        self._docker_client.exec_service(
            LAB_SHELL_CONTAINER_NAME,
            env={
                'LAB_VERSION': config.version(),
                'LAB_WORKSPACE': config.workspace(),
                'LAB_WORKSPACE_DATA': config.workspace_data(),
                'LAB_CICD_ARTIFACT_STORAGE': config.cicd_storage_path(),
                'LAB_ROLE_LABEL': config.lab_role_label(),
                'LAB_SHELL_ROLE': config.lab_shell_role()
            }
        )
