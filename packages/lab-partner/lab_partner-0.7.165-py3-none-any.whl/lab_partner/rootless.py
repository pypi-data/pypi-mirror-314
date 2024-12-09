import os
import pathlib
import logging
import sys
import time
import itertools
from subprocess import CalledProcessError

from . import user_info
from .docker import (
    DockerClient,
    DockerComposeClient,
    DockerEnvironment,
    FilterSet,
    LabelFilter,
    StatusFilter,
    DockerContainerStatus
)
from .process_utils import run_process_quiet
from . import config


logger = logging.getLogger(__name__)


LAB_ROOTLESS_INIT = 'lab-rootless-init'
LAB_ROOTLESS_DOCKERD = 'lab-rootless-dockerd'
LAB_ROOTLESS_STORAGE = 'lab-rootless-storage'
LAB_ROOTLESS_USER_STORAGE = 'lab-rootless-user-storage'
LAB_ROOTLESS_COMPOSE_CONFIG_PATH = 'lab_partner.compose_config.rootless'
LAB_ROOTLESS_COMPOSE_INIT_FILENAME = 'docker-compose-init.yml'
LAB_ROOTLESS_COMPOSE_ROOTLESS_FILENAME = 'docker-compose-rootless.yml'

WAITING_ANIMATION_FRAMES = itertools.cycle(['|', '/', '—', '\\'])


class RootlessContainer:
    def __init__(self, env: DockerEnvironment):
        self.container_name = LAB_ROOTLESS_DOCKERD
        self._docker_client = DockerClient(env)
        self._rootless_docker_client = DockerClient(self.rootless_env())
        self._compose_client = DockerComposeClient(config.project_name(), LAB_ROOTLESS_COMPOSE_CONFIG_PATH, env)
        self._role_label_filter = LabelFilter(config.lab_role_label(), config.lab_container_runtime_role())

    def does_rootless_container_exist(self) -> bool:
        """Test if the rootless container exists in any state on the daemon

        :return: True if a container is found with expected name
        """
        return self._docker_client.has_containers(FilterSet().add_filter(self._role_label_filter))

    def is_rootless_container_running(self) -> bool:
        """Test if the rootless container is running on the daemon

        :return: True if the container is found with the expected name and in the "running" state
        """
        filters = FilterSet().add_filter(self._role_label_filter).add_filter(StatusFilter(DockerContainerStatus.RUNNING))
        return self._docker_client.has_containers(filters)

    def start(self) -> None:
        """Run the sequence of steps to start a rootless docker daemon

        1. Check if rootless is already running. If so then return it.
        2. Create a named volume to store CI/CD artifacts for Act
        3. Finally start a new rootless container

        :param workspace_path: path of the host workspace to bind mount
        :return: DockerDaemonInfo of newly started rootless daemon
        """
        if self.is_rootless_container_running():
            logger.debug('Rootless container already running')
            return

        logger.info('Starting rootless container. It can take a couple minutes to start')
        self._init_rootless()
        self._start_rootless()
        self._rootless_docker_client.create_network(config.lab_network_name())

    def _init_rootless(self) -> None:
        """Create a user accessible named volumed

        Named volumes get create as root. This changes the ownership
        to be "rootless" in order for it to properly get mapped to
        the host user

        :param name: name of the named volume to create
        """
        logger.debug('Intializing rootless environment')
        self._compose_client.run_service(
            LAB_ROOTLESS_INIT,
            LAB_ROOTLESS_COMPOSE_INIT_FILENAME,
            env={
                'LAB_CICD_ARTIFACT_STORAGE': config.cicd_storage_path()
            }
        )

    def _start_rootless(self) -> None:
        """Start rootless container and wait for it to be ready

        :param workspace_path: path of the host workspace to bind mount
        :return: DockerDaemonInfo of newly started rootless daemon
        """
        logger.debug('Starting rootless')
        pathlib.Path(config.cicd_storage_path_host_path()).mkdir(parents=True, exist_ok=True)
        self._compose_client.start_service(
            LAB_ROOTLESS_DOCKERD,
            LAB_ROOTLESS_COMPOSE_ROOTLESS_FILENAME,
            env={
                'HOME': user_info.home(),
                'USER': user_info.username(),
                # 'UID': str(self._user_info.uid()),
                # 'GID': str(self._user_info.gid()),
                'LAB_VERSION': config.version(),
                'LAB_WORKSPACE': config.workspace(),
                'LAB_CICD_ARTIFACT_STORAGE': config.cicd_storage_path(),
                'XDG_RUNTIME_DIR': user_info.user_runtime_tmp_path(),
                'LAB_ROLE_LABEL': config.lab_role_label(),
                'LAB_CONTAINER_RUNTIME_ROLE': config.lab_container_runtime_role()
            }
        )
        # run_rootless_docker_cmd = DockerRunBuilder(self._rootless_docker_image())
        # run_rootless_docker_cmd.options() \
        #     .with_name(self.container_name) \
        #     .with_hostname(self.container_name) \
        #     .with_privileged() \
        #     .with_host_ipc() \
        #     .with_daemon() \
        #     .with_current_user() \
        #     .with_env('POOL_BASE', '172.28.0.0/16') \
        #     .with_env('POOL_SIZE', '21') \
        #     .with_port_mapping(80, 80) \
        #     .with_bind_mount(workspace_path, workspace_path) \
        #     .with_bind_mount('/tmp', '/tmp') \
        #     .with_bind_mount('/dev', '/dev') \
        #     .with_named_volume(LAB_ROOTLESS_STORAGE, '/var/lib/docker') \
        #     .with_named_volume(LAB_ROOTLESS_USER_STORAGE, '/home/rootless/.local/share/docker') \
        #     .with_named_volume(LAB_CICD_ARTIFACT_STORAGE, '/opt/lab/cicd/artifacts') \
        #     .with_mount_home() \
        #     .with_mount_user_run()
        # rendered_cmd = run_rootless_docker_cmd.build()
        # logger.debug(rendered_cmd)
        # for log_line in run_process(rendered_cmd):
        #     logger.info(log_line)
        self._wait_for_rootless()

    def _wait_for_rootless(self, timeout: int = 120) -> None:
        """Waits for rootless container to start accepting API calls

        :param timeout: number of seconds to wait for, defaults to 120
        :raises TimeoutError: timeout error raised when exeeds timeout
        """
        start_time = time.perf_counter()
        while True:
            if not self.is_rootless_container_running():
                time.sleep(1)
                continue
            try:
                run_process_quiet('docker info', {'DOCKER_HOST': self._rootless_docker_url()})
                break
            except CalledProcessError as ex:
                elapsed_time = time.perf_counter() - start_time
                sys.stdout.write(f'{next(WAITING_ANIMATION_FRAMES)} Waiting for rootless docker to start\r')
                sys.stdout.flush()
                if elapsed_time >= timeout:
                    raise TimeoutError(f'Timeout waiting for rootless docker after {timeout} seconds', ex)
                time.sleep(.1)

    def stop(self) -> None:
        if not self.is_rootless_container_running():
            logger.debug('Rootless container is not running')
            return

        logger.debug('About to stop rootless')
        pathlib.Path(config.cicd_storage_path_host_path()).mkdir(parents=True, exist_ok=True)
        self._compose_client.stop_service(
            LAB_ROOTLESS_DOCKERD,
            LAB_ROOTLESS_COMPOSE_ROOTLESS_FILENAME,
            env={
                'HOME': user_info.home(),
                'USER': user_info.username(),
                # 'UID': str(self._user_info.uid()),
                # 'GID': str(self._user_info.gid()),
                'LAB_VERSION': config.version(),
                'LAB_WORKSPACE': config.workspace(),
                'LAB_CICD_ARTIFACT_STORAGE': config.cicd_storage_path(),
                'XDG_RUNTIME_DIR': user_info.user_runtime_tmp_path(),
                'LAB_ROLE_LABEL': config.lab_role_label(),
                'LAB_CONTAINER_RUNTIME_ROLE': config.lab_container_runtime_role()
            }
        )

    @staticmethod
    def _rootless_docker_image() -> str:
        """Build the docker images name based on the python
        package version

        :return: name of the rootless docker image to use
        """
        return f'enclarify/lab-partner-dind-rootless:{config.version()}'

    @staticmethod
    def _rootless_docker_url() -> str:
        """Construct the rootless docker file socket url
        based on XDG_RUNTIME_DIR environment variable. Likely needs to be
        fixed for other platforms like mac

        :return: rootless file socket url
        """
        xdg_runtime_dir = os.environ['XDG_RUNTIME_DIR']
        return f'unix://{xdg_runtime_dir}/docker.sock'

    @classmethod
    def rootless_env(cls) -> DockerEnvironment:
        return DockerEnvironment.build_with_overridden_host(cls._rootless_docker_url())
