import os
import logging
from pathlib import Path
from typing import List, Optional, Set

from lab_partner.option_set import Option, OptionSet
from ..user_info import UnixUser


logger = logging.getLogger(__name__)


class InvalidDockerOptionConfiguration(Exception):
    pass


def environment_variable_renderer(key: str, value: Optional[str] = None) -> str:
    if value:
        return f'{key}={value}'
    else:
        return key

def named_volume_mount_renderer(key: str, value: str):
    return f'type=volume,src={key},dst={value}'

def bind_mount_render(key: str, value: str):
    return f'type=bind,src={key},dst={value}'


class DockerRunOptions:
    """
    This class helps build up a list of options for the invocation of Docker.
    """
    def __init__(self):
        self._options = OptionSet()
        self._tty_option = Option('-it')
        self._daemon_option = Option('-d')
        self._options.add_mutually_exclusive_options((self._tty_option, self._daemon_option))
        self._user_info = UnixUser()

    def with_init(self) -> 'DockerRunOptions':
        """Add the '--init' option to run Tini to manage the
        main process

        :return: this DockerRunOptions instance
        """
        self._options.put_option('--init')
        return self

    def with_remove_on_exit(self) -> 'DockerRunOptions':
        """Add the '--rm' option to remove the container 
        after exiting

        :return: this DockerRunOptions instance
        """
        self._options.put_option(f'--rm')
        return self

    def with_name(self, name: str) -> 'DockerRunOptions':
        """Add the '--name' option to name the container

        :param name: name of the container
        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--name', name)
        return self

    def with_hostname(self, hostname: str) -> 'DockerRunOptions':
        """Add the '--hostname' option to set the container
        hostname

        :param hostname: hostname of the container
        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--hostname', hostname)
        return self
    
    def with_user(self, uid: int, gid: int) -> 'DockerRunOptions':
        """Add the '--user' option to run the container 
        as a specific user and group

        :param uid: UID of the user to run as
        :param gid: GID of the user to run as
        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--user', f'{uid}:{gid}')
        return self

    def with_current_user(self) -> 'DockerRunOptions':
        """Add the '--user' option with the current
        user and group

        :return: this DockerRunOptions instance
        """
        return self.with_user(self._user_info.uid, self._user_info.gid)
    
    def with_root_user(self) -> 'DockerRunOptions':
        """Add the '--user' option with the 0 as the UID and GID to force
        running as root

        :return: this DockerRunOptions instance
        """
        return self.with_user(0, 0)

    def with_privileged(self) -> 'DockerRunOptions':
        """Add the '--privileged' flag to run the container with no limitations

        :return: this DockerRunOptions instance
        """
        self._options.put_option('--privileged')
        return self
    
    def with_host_ipc(self) -> 'DockerRunOptions':
        """Add the '--ipc' option set to 'host' to share all IPC resources

        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--ipc', 'host')
        return self

    def with_tty(self) -> 'DockerRunOptions':
        """Add the '-it' option to start interactive TTY

        :return: this DockerRunOptions instance
        """
        self._options.put(self._tty_option)
        return self

    def with_daemon(self) -> 'DockerRunOptions':
        """Add the '-d' option to start in daemon mode

        :return: this DockerRunOptions instance
        """
        self._options.put(self._daemon_option)
        return self

    def with_network(self, network_name: str) -> 'DockerRunOptions':
        """Add the '--network' option to specify the network name

        :param network_name: name of the network
        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--network', network_name)
        return self

    def with_workdir(self, workdir: str) -> 'DockerRunOptions':
        """Add the '--workdir' option to specify the current working dirtory 

        :param workdir: path to current working directory
        :return: this DockerRunOptions instance
        """
        self._options.put_value_option('--workdir', workdir)
        return self

    def with_env(self, key: str, value: Optional[str] = None) -> 'DockerRunOptions':
        """Add the '-e' environment value option to set environment key/value pairs. However,
        docker does allow environment variables to set without values if they are currently set
        as a shortcut. 

        :param key: Environment variable name
        :param value: Environment variable value
        :return: this DockerRunOptions instance
        """
        self._options.put_key_value_option('-e', key, value, environment_variable_renderer)
        return self

    def with_mount_user_run(self) -> 'DockerRunOptions':
        """Add the '--mount' option as a bind mount of the user run path of the 
        system. This is the same as XDG_RUNTIME_DIR on a linux system.

        :return: this DockerRunOptions instance
        """
        self._options.put_key_value_option('--mount', f'/run/user/{self._user_info.uid}/', f'/run/user/{self._user_info.uid}/', bind_mount_render)
        return self

    def with_mount_home(self) -> 'DockerRunOptions':
        """Add the '--mount' option as a bind mount of the user runtime path of the 
        system. This is the same as XDG_RUNTIME_DIR on a linux system.

        :return: this DockerRunOptions instance
        """
        self._options.put_key_value_option('--mount', self._user_info.home, self._user_info.home, bind_mount_render)
        return self

    def with_home_dir_bind_mount(self, source: str, target: str, validate_source_exists: bool = True) -> 'DockerRunOptions':
        source_in_home = self._user_info.home_subdir(source)
        if source and target and self._path_exists(source_in_home, validate_source_exists):
            self._options.put_key_value_option('--mount', source_in_home, target, bind_mount_render)
        else:
            logger.warning(f'Requested HOME mount that does not exist: {source_in_home}')
        return self

    def with_bind_mount(self, source: str, target: str) -> 'DockerRunOptions':
        """Adds an option to bind mount a host volume

        :param source: Source host path to be mounted
        :param target: Target path inside container to attach the mount
        :return: self
        """
        self._options.add(f'-v {source}:{target}')
        return self

    def with_named_volume(self, name: str, target: str) -> 'DockerRunOptions':
        self._options.add(f'--mount type=volume,src={name},dst={target}')
        return self

    def with_port_mapping(self, external_port: int, internal_port: int) -> 'DockerRunOptions':
        self._options.add(f'-p {external_port}:{internal_port}')
        return self
    
    def with_entrypoint(self, entrypoint: str) -> 'DockerRunOptions':
        self._options.add(f'--entrypoint={entrypoint}')
        return self

    def build(self) -> str:
        """Builds the accumulated options into a space-separated string.

        :return: String containing all the options.
        """
        return str(self._options)

    @staticmethod
    def _path_exists(path: str, should_validate: bool) -> bool:
        """Check for the existence of a source path

        :param path: Path to be checked
        :param should_validate: Whether we should really check.  If False, the method
        will return True regardless of whether the path exists.
        :return:
        """
        if not should_validate:
            return True
        else:
            return Path(path).exists()
    

class DockerRunBuilder(object):
    def __init__(self, image_name: str, command: str = ''):
        self._image_name = image_name
        self._command = command
        self._options = DockerRunOptions()

    def options(self):
        return self._options

    def build(self) -> str:
        return f'docker run \
                {self._options.build()} \
                {self._image_name} \
                {self._command}'
