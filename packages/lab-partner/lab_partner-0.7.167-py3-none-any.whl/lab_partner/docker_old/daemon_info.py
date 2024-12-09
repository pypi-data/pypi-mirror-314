import logging
from typing import Dict, Any, List, Optional
import json

from ..user_info import UnixUser
from ..process_utils import (
    run_process,
    run_process_single_result,
    process_output_as_json
)
from ..config import is_linux


logger = logging.getLogger(__name__)


class DockerDaemonInfo:
    def __init__(self, docker_host: Optional[str] = None):
        self._env = {}
        if docker_host:
            self._env = {'DOCKER_HOST': docker_host}
            logger.debug(f'DOCKER_HOST={docker_host}')
        self._info = self._read_daemon_info(self._env)
        logger.debug(f'Daemon Info: {self._info}')
        self._user_info = UnixUser()

    def is_rootless(self) -> bool:
        """
        Detects rootless docker security option
        :return: boolean of rootless or not
        """
        if 'SecurityOptions' not in self._info:
            logger.error("Unable to determine docker security options. Is the daemon running properly?")
            raise ValueError("Unable to determine docker security options. Is the daemon running properly?")

        sec_options = self._info['SecurityOptions']
        if sec_options:
            for opt in sec_options:
                if 'rootless' in opt:
                    return True
        return False

    def docker_socket(self) -> str:
        """
        Returns the path to the Docker socket
        :return:
        """
        if is_linux():
            if self.is_rootless():
                return f'/run/user/{self._user_info.uid}/docker.sock'
            else:
                return '/run/docker.sock'
        else:
            return '/var/run/docker.sock.raw'

    def docker_internal_socket(self) -> str:
        """
        Returns the path to the Docker socket that should be use when launching
        containers from inside the CLI that need to mount the docker socket
        :return:
        """
        if self.is_rootless():
            return f'/run/user/{self._user_info.uid}/docker.sock'
        else:
            return '/run/docker.sock'

    def network_exists(self, network_name: str) -> bool:
        for net in self.networks:
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
            rs = run_process(f'docker network create {network_name}', self._env)
            for line in rs:
                logger.debug(line)
        else:
            logger.debug(f'Network {network_name} already exists')

    def volume_exists(self, volume_exists: str) -> bool:
        for net in self.networks:
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
            rs = run_process(f'docker volume create {name}', self._env)
            for line in rs:
                logger.debug(line)
            return True
        else:
            logger.debug(f'Volume "{name}" already exists')
            return False

    @property
    def info(self) -> Dict[str, Any]:
        return self._info

    def containers(self) -> List[Dict[str, Any]]:
        rs = run_process('docker container ls -a --format "{{json .}}"', self._env)
        conts = process_output_as_json(rs)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Docker containers:')
            for c in conts:
                logger.debug(c)
        return conts

    @property
    def networks(self) -> List[Dict[str, Any]]:
        rs = run_process('docker network ls --format "{{json .}}"', self._env)
        nets = process_output_as_json(rs)
    
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Docker networks:')
            for n in nets:
                logger.debug(n)
        return nets
    
    @property
    def volumes(self) -> List[Dict[str, Any]]:
        rs = run_process('docker volume ls --format "{{json .}}"', self._env)
        vols = process_output_as_json(rs)
    
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Docker volumes:')
            for n in vols:
                logger.debug(n)
        return vols

    @classmethod
    def build(cls) -> 'DockerDaemonInfo':
        return DockerDaemonInfo()

    @classmethod
    def build_with_docker_host(cls, docker_host: str) -> 'DockerDaemonInfo':
        return DockerDaemonInfo(docker_host=docker_host)

    @staticmethod
    def _read_daemon_info(env: Optional[Dict[str,str]]) -> Dict[str, Any]:
        """
        Returns the output of `docker info` as a dictionary
        :return:
        """
        info_str = run_process_single_result('docker info --format "{{json .}}"', env)
        return json.loads(info_str)


