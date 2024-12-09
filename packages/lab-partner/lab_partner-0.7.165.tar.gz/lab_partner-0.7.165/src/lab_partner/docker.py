from enum import Enum
import json
import logging
from typing import Any, Dict, List, Optional, Set
from importlib.resources import files
from lab_partner.process_utils import (
    process_output_as_json,
    run_process,
    run_process_single_result,
    exec_process,
    run_process_stream_result
)

logger = logging.getLogger(__name__)


class FilterOperator(Enum):
    EQUAL = '='
    NOT_EQUAL = '!='


class DockerContainerStatus(Enum):
    CREATED = 'created'
    RUNNING = 'running'
    PAUSED = 'paused'
    RESTARTING = 'restarting'
    EXITED = 'exited'
    REMOVING = 'removing'
    DEAD = 'dead'


class LabelFilter:
    def __init__(
            self, key: str, value: Optional[str] = None,
            key_operator: FilterOperator = FilterOperator.EQUAL,
            value_operator: FilterOperator = FilterOperator.EQUAL) -> None:
        self._key = key
        self._value = value
        self._key_operator = key_operator
        self._value_operator = value_operator

    def __str__(self) -> str:
        s = 'label' + self._key_operator.value + self._key
        if self._value:
            s += self._value_operator.value + self._value
        return s


class StatusFilter:
    def __init__(self, status: DockerContainerStatus, operator: FilterOperator = FilterOperator.EQUAL) -> None:
        self._status = status
        self._operator = operator

    def __str__(self) -> str:
        return 'status' + self._operator.value + self._status.value


class FilterSet:
    def __init__(self) -> None:
        self._options: Set[StatusFilter | LabelFilter] = set()

    def add_filter(self, filter: StatusFilter | LabelFilter) -> 'FilterSet':
        self._options.add(filter)
        return self

    def __str__(self) -> str:
        return ' '.join(map(lambda x: '-f ' + str(x), self._options))


class DockerEnvironment:
    def __init__(self, initial_env: Optional[Dict[str, str]] = None) -> None:
        self._env = initial_env or {}

    def put(self, env: Optional[Dict[str, str]]) -> 'DockerEnvironment':
        return DockerEnvironment({**self._env, **(env or {})})

    def as_dict(self) -> Dict[str, str]:
        return self._env

    @staticmethod
    def build_with_overridden_host(docker_host: str):
        return DockerEnvironment({'DOCKER_HOST': docker_host})


class DockerComposeClient:
    def __init__(self, project_name: str, config_root_path: str, env: DockerEnvironment) -> None:
        self._project_name = project_name
        self._config_root_path = config_root_path
        self._env = env

    def exec_service(self, service_name: str, config_filename: str = 'docker-compose.yml', env: Optional[Dict[str, str]] = None) -> None:
        config = files(self._config_root_path).joinpath(config_filename)
        cmd = f'docker compose -f {config} -p {self._project_name} run --remove-orphans {service_name}'
        logger.debug(cmd)
        exec_process(cmd, env=self._env.put(env).as_dict())

    def run_service(self, service_name: str, config_filename: str = 'docker-compose.yml', env: Optional[Dict[str, str]] = None) -> None:
        config = files(self._config_root_path).joinpath(config_filename)
        cmd = f'docker compose -f {config} -p {self._project_name} run -T --remove-orphans {service_name}'
        logger.debug(cmd)
        logs = run_process_stream_result(cmd, env=self._env.put(env).as_dict())
        for log in logs:
            logger.info(log)

    def start_service(self, service_name: str, config_filename: str = 'docker-compose.yml', env: Optional[Dict[str, str]] = None) -> None:
        config = files(self._config_root_path).joinpath(config_filename)
        cmd = f'docker compose -f {config} -p {self._project_name} up -d --remove-orphans --force-recreate --no-build {service_name}'
        logger.debug(cmd)
        logs = run_process_stream_result(cmd, env=self._env.put(env).as_dict())
        for log in logs:
            logger.info(log)

    def stop_service(self, service_name: str, config_filename: str = 'docker-compose.yml', env: Optional[Dict[str, str]] = None):
        config = files(self._config_root_path).joinpath(config_filename)
        cmd = f'docker compose -f {config} -p {self._project_name} stop {service_name}'
        logger.debug(cmd)
        logs = run_process_stream_result(cmd, env=self._env.put(env).as_dict())
        for log in logs:
            logger.info(log)


class DockerClient:
    def __init__(self, env: DockerEnvironment):
        self._env = env

    def network_exists(self, network_name: str) -> bool:
        for net in self.read_networks():
            if network_name == net['Name']:
                return True
        return False

    def create_network(self, network_name: str) -> None:
        """
        Creates a bridged network
        :return: None
        """
        if not self.network_exists(network_name):
            logger.info(f'Creating network: {network_name}')
            cmd = f'docker network create {network_name}'
            rs = run_process(cmd, self._env.as_dict())
            for line in rs:
                logger.debug(line)
        else:
            logger.debug(f'Network {network_name} already exists')

    def volume_exists(self, volume_exists: str) -> bool:
        for net in self.read_volumes():
            if volume_exists == net['Name']:
                return True
        return False

    def create_volume(self, name: str) -> bool:
        """Create a named volume if it doesn't already exist

        :param name: name of the volume to create
        :return: was a volume created?
        """
        if not self.volume_exists(name):
            logger.info(f'Creating volume: {name}')
            rs = run_process(f'docker volume create {name}', self._env.as_dict())
            for line in rs:
                logger.debug(line)
            return True
        else:
            logger.debug(f'Volume "{name}" already exists')
            return False

    def read_daemon_info(self) -> Dict[str, Any]:
        """
        Returns the output of `docker info` as a dictionary
        :return:
        """
        info_str = run_process_single_result('docker info --format "{{json .}}"', self._env.as_dict())
        return json.loads(info_str)

    def has_containers(self, filters: Optional[FilterSet] = None) -> bool:
        return True if self.read_containers(filters) else False

    def read_containers(self, filters: Optional[FilterSet] = None) -> List[Dict[str, Any]]:
        filters_str = str(filters) if filters else ''
        cmd = 'docker container ls -a --format "{{json .}}"'
        rs = run_process(' '.join([cmd, filters_str]), self._env.as_dict())
        containers = process_output_as_json(rs)
        logger.debug('Docker containers:')
        logger.debug(containers)
        return containers

    def kill_container(self, container_name: str) -> None:
        for log_line in run_process(f'docker rm -f {container_name}'):
            logger.info(log_line)

    def read_networks(self) -> List[Dict[str, Any]]:
        rs = run_process('docker network ls --format "{{json .}}"', self._env.as_dict())
        nets = process_output_as_json(rs)
        logger.debug('Docker networks:')
        logger.debug(nets)
        return nets

    def read_volumes(self) -> List[Dict[str, Any]]:
        rs = run_process('docker volume ls --format "{{json .}}"', self._env.as_dict())
        vols = process_output_as_json(rs)
        logger.debug('Docker volumes:')
        logger.debug(vols)
        return vols
