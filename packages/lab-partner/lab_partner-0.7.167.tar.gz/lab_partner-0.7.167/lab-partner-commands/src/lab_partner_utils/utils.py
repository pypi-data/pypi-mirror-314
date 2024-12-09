import logging
import os
import sys
from typing import Dict, Tuple, Optional
import subprocess
import click
from click import Context
from dotenv import dotenv_values
from docker import APIClient


logger = logging.getLogger(__name__)


class WorkspaceEntryPointMetadata(object):
    """
    Scans the workspace looking for specific entry points able to be
    parsed for CLI commands to dynamically add
    """

    def __init__(self, name: str, value: str, script_name: str, function_name: str,
                 project_name: str, project_version: str, project_path: str, project_data_path: Optional[str] = None):
        """
        Constructor

        :param name: parsed name of the cli_plugins entry point
        :param value: parsed value of the cli_plugins entry point
        :param script_name: parsed script name of the cli_plugins entry point
        :param function_name: parsed function name of the cli_plugins entry point
        :param project_name: name of the project based on the directory the pyproject.toml is found in
        :param project_version: version as found in the pyproject.toml
        :param project_path: path of the project in the workspace containing a cli_plugins
        :param project_data_path: path to an optional 'data' folder in the project
        """
        self.name = name
        self.value = value
        self.script_name = script_name
        self.function_name = function_name
        self.project_name = project_name
        self.project_version = project_version
        self.project_path = project_path
        self.project_data_path = project_data_path

    @staticmethod
    def from_context(ctx: Context) -> 'WorkspaceEntrypointMetadata':
        return WorkspaceEntryPointMetadata(
            ctx.meta['name'],
            ctx.meta['value'],
            ctx.meta['script_name'],
            ctx.meta['function_name'],
            ctx.meta['project_name'],
            ctx.meta['project_version'],
            ctx.meta['project_path'],
            ctx.meta['project_data_path'])

    @classmethod
    def build(cls, entry_point_name: str, entry_point_value: str, project_name: str, project_version: str, project_path: str, project_data_path: str) -> 'WorkspaceEntrypointMetadata':
        """
        Static builder. Parses a raw entry point string and builds a WorkspaceEntrypointMetadata

        :param entry_point_name: name of the entry-point in a pyproject.toml file
        :param entry_point_value: value of the entry-point in a pyproject.toml file
        :param project_name: name of the directory the pyproject.toml is found in
        :param project_version: version as found in the pyproject.toml
        :param project_path: path of the project in the workspace containing a cli_plugins
        :param project_data_path: path to an optional 'data' folder in the project
        :return:
        """
        cls._validate_entry_point_value(entry_point_name, entry_point_value)
        script_name, function_name = cls._parse_entry_point_value(entry_point_value)
        return WorkspaceEntryPointMetadata(entry_point_name, entry_point_value, script_name, function_name,
                                           project_name, project_version, project_path, project_data_path)

    @staticmethod
    def _validate_entry_point_value(entry_point_name: str, entry_point_value: str) -> None:
        """
        Validates a raw entry point string to ensure it is well-formed and
        raises a ValueError if not

        Should be of the form:
            <command-name> = <folder_name>.<script_name>:<function_name>

        :param entry_point_value: raw entry point string in a pyproject.toml file
        """
        # TODO make if condition use a proper regex for the format below
        if ':' not in entry_point_value:
            error_message = f'''
            !----------------------------------------------------
            Found CLI plugin entry point of:
                {entry_point_name} = "{entry_point_value}"

            CLI plugin entry point not well formed. Should be of the form:
                <command-name> = "<folder_name>.<script_name>:<function_name>"

            For example: 
                example = "example_project_command_set:example"

            The <folder_name> is optional
            !---------------------------------------------------- 
            '''
            raise ValueError(error_message)

    @staticmethod
    def _parse_entry_point_value(entry_point_value: str) -> Tuple[str, str]:
        """
        Parse entry point value string into a tuple of:
            script name
            function name

        :param entry_point_value: entry point value string in a pyproject.toml file
        :return:
        """
        script_path, function_name = entry_point_value.split(':')
        script_path_parts = script_path.split('.')
        script_name = script_path_parts[-1]
        return script_name, function_name


def print_subprocess_output(rs: subprocess.CompletedProcess) -> None:
    """
    Prints stdout of subprocess

    :param rs: a CompletedProcess to print stdout from
    """
    if rs.returncode == 0:
        click.echo(rs.stdout.decode('utf-8'))
    else:
        click.echo(rs.stderr.decode('utf-8'))


def print_docker_build_logs(logs) -> None:
    for chunk in logs:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                click.echo(line)


def build_docker_api_client() -> APIClient:
    docker_url = 'unix://var/run/docker.sock'
    # allows DOCKER_HOST set in the environment to override using the default host
    # docker socket to run the docker commands
    if 'DOCKER_HOST' in os.environ:
        docker_url = os.environ['DOCKER_HOST']
    return APIClient(base_url=docker_url)


def expand_variables(content: str, replace_vars: Dict[str, str]) -> str:
    """
    Does string variable replacement for bash-like variable tokens of the form $VAR or ${VAR}

    :param content: The string to find bash-like variable tokens in
    :param replace_vars: a dictionary of the variable names and values to replace if found
    :return: a string with the bash-like tokens replaced
    """
    for k, v in replace_vars.items():
        if v:
            content = content.replace('$' + k, v)
            content = content.replace('${' + k + '}', v)
    return content


def parse_image_name(image_name: str) -> Tuple[str, str, str]:
    """
    Parses a docker image name into a tuple of registry name, image name and image version

    :param image_name: full docker image name
    :return: tuple of registry name, image name and image version
    """
    if '/' in image_name:
        image_name_parts = image_name.split('/')
        registry_name = image_name_parts[0]
        root_image_name = image_name_parts[1].split(':')[0]
    else:
        registry_name = None
        root_image_name = image_name.split(':')[0]
    image_version = image_name.split(':')[1]
    return registry_name, root_image_name, image_version


def read_env(workspace_metadata: WorkspaceEntryPointMetadata, env_path: Optional[str] = None) -> Dict[str, str]:
    """
    Reads and merges different sets of environment variables that will be leveraged when starting or stopping services

    :param workspace_metadata: metadata for the workspace of the project
    :param env_path: environment variable file path
    :return:
    """
    env = {
        'DISPLAY': os.environ['DISPLAY'],
        'LAB_DOCKER_SOCKET': os.environ['LAB_DOCKER_SOCKET'],
        'LAB_ROOT': os.environ['LAB_ROOT'],
        'LAB_HOME': os.environ['LAB_HOME'],
        'LAB_NETWORK_NAME': os.environ['LAB_NETWORK_NAME'],
        'LAB_VERSION': os.environ['LAB_VERSION'],
        'LAB_PROJECT_WORKSPACE': workspace_metadata.project_path,
        'LAB_PROJECT_WORKSPACE_DATA': workspace_metadata.project_data_path
    }

    set_env_if_exists(env, 'AWS_ACCESS_KEY_ID')
    set_env_if_exists(env, 'AWS_SECRET_ACCESS_KEY')
    set_env_if_exists(env, 'AWS_SESSION_TOKEN')
    set_env_if_exists(env, 'DOCKER_HOST')

    if env_path:
        absolute_env_path = os.path.join(workspace_metadata.project_path, env_path)
        env_file_vars = dotenv_values(absolute_env_path)
        env.update(env_file_vars)
    return env


def set_env_if_exists(env: dict, env_name: str) -> None:
    if env_name in os.environ:
        env[env_name] = os.environ[env_name]


def read_docker_compose_config(workspace_metadata: WorkspaceEntryPointMetadata,
                               compose_config_path: str, env: Dict[str, str]) -> str:
    """
    Reads a docker compose file, replaces any environment variables defined

    :param workspace_metadata: metadata for the workspace of the project
    :param compose_config_path: file system path to a docker compose file
    :param env: environment variable file path
    :return:
    """
    try:
        absolute_config_path = os.path.join(workspace_metadata.project_path, compose_config_path)
        with open(absolute_config_path, 'r') as config:
            prepared_config = expand_variables(config.read(), env)
        rs = subprocess.run(['docker-compose', '-f', '-', 'config'], input=prepared_config.encode(), capture_output=True)
        err = rs.stderr.decode('utf-8')
        if err:
            click.echo(err)
        processed_config = rs.stdout.decode('utf-8')
        return processed_config
    except subprocess.CalledProcessError as e:
        click.echo(e.stderr)
        sys.exit('Error parsing docker-compose.yml')


def exec_compose(compose_cmd: str, compose_config_content: str, env: Optional[Dict[str, str]]=None) -> None:
    """
    Exec a docker compose process by forking the current process allowing the child
    to take over the main process id

    :param compose_cmd: any docker compose command
    :param compose_config_content: a string representation of the contents of a docker compose file
    """
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Child process
        os.dup2(r, sys.stdin.fileno())
        os.close(r)
        os.close(w)
        up_command = f'docker-compose -f - {compose_cmd}'.split()
        if env:
            os.execvpe(up_command[0], up_command, env)
        else:
            os.execvp(up_command[0], up_command)
    else:
        # Parent process
        os.close(r)
        os.write(w, bytearray(compose_config_content, 'utf-8'))
        os.close(w)
        pid, status = os.waitpid(pid, 0)


def start_compose(project_name: str, services: str, compose_config_content: str, env: Optional[Dict[str, str]]=None):
    exec_compose(f'-p {project_name} up -d --force-recreate {services}', compose_config_content, env)


def stop_compose(project_name: str, services: str, compose_config_content: str, env: Optional[Dict[str, str]]=None):
    exec_compose(f'-p {project_name} rm --force --stop -v {services}', compose_config_content, env)


def start_services(workspace_metadata: WorkspaceEntryPointMetadata,
                   env_path: Optional[str] = None,
                   compose_config_path: str = 'docker-compose.yml',
                   services: str = '',
                   create_data_directory: bool = True,
                   env_override: Optional[Dict[str, str]]=None) -> None:
    """
    Start services defined in docker compose file

    :param workspace_metadata: metadata for the workspace of the project
    :param env_path: environment variable file path
    :param compose_config_path: a docker compose config file path
    :param services: comma separated list of services to start or omit param to start all
    :param create_data_directory: comma separated list of services to start or omit param to start all
    """
    if create_data_directory and workspace_metadata.project_data_path:
        os.makedirs(workspace_metadata.project_data_path, exist_ok=True)
    elif create_data_directory:
        os.makedirs(os.path.join(workspace_metadata.project_path, 'data'), exist_ok=True)
    env = read_env(workspace_metadata, env_path)
    if env_override:
        env.update(env_override)
    config = read_docker_compose_config(workspace_metadata, compose_config_path, env)
    start_compose(workspace_metadata.project_name, services, config, env)


def stop_services(workspace_metadata: WorkspaceEntryPointMetadata,
                  env_path: Optional[str] = None,
                  compose_config_path: str = 'docker-compose.yml',
                  services: str = '') -> None:
    """
    Stop services running in docker compose

    :param workspace_metadata: metadata for the workspace of the project
    :param env_path: environment variable file path
    :param compose_config_path: a docker compose config file path
    :param services: comma separated list of services to start or omit param to start all
    """
    env = read_env(workspace_metadata, env_path)
    config = read_docker_compose_config(workspace_metadata, compose_config_path, env)
    stop_compose(workspace_metadata.project_name, services, config, env)
