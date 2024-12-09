import os
from typing import Dict, Optional, List, Callable, Any
import sys
import logging

import click
from click import Command, Context, MultiCommand, CommandCollection
from ..utils import WorkspaceEntryPointMetadata
from . import (
    CLI_PLUGINS_ENTRY_POINT,
    CLI_WORKSPACE_ONLY_PLUGINS_ENTRY_POINT
)
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


WORKSPACE_PATH = os.environ['LAB_WORKSPACE']
WORKSPACE_DATA_PATH = os.path.join(WORKSPACE_PATH, 'data')


logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)


class WorkspaceEntrypointCommands(MultiCommand):
    def list_commands(self, ctx: Context) -> List[str]:
        """
        Generates list of subcommand names by scanning the workspace for cli_plugins entry point

        :param ctx: current click context
        :return: list of subcommand names
        """
        click.echo('here')
        raise ValueError('list commands')
        found_cli_plugins = self._cli_plugin_search(WORKSPACE_PATH)
        plugin_names = []
        if found_cli_plugins:
            plugin_names = list(found_cli_plugins.keys())
            plugin_names.sort()
        return plugin_names

    def get_command(self, ctx: Context, project_name: str) -> Optional[Command]:
        """
        Builds a set of commands for a specific project and returns a click Command

        :param ctx: current click context
        :param project_name: name of the scanned project with CLI an entry point
        :return: Compiled click Command or None if there was an error
        """
        click.echo('here')
        raise ValueError('list commands')
        found_cli_plugins = self._cli_plugin_search(WORKSPACE_PATH)
        if project_name not in found_cli_plugins:
            return None

        plugin_metadata = found_cli_plugins[project_name]
        plugin_script_path = self._absolute_script_path(plugin_metadata.project_path, plugin_metadata.script_name)
        if not plugin_script_path:
            logger.error(
                f'Error: project "{project_name}" supplies a CLI plugin but script "{plugin_metadata.script_name}" could not be loaded')
            return None
        ctx.meta.update(plugin_metadata.__dict__)
        return self.compile_command(plugin_script_path, plugin_metadata.function_name)

    @staticmethod
    def compile_command(plugin_script_path, function_name) -> Optional[Command]:
        """
        Compiles click Command from the specified script path. This allows discovered workspace
        commands to be used on the fly

        :param plugin_script_path: absolute path to the script file to compile
        :param function_name: name of the function to pull the compiled command out of scope
        :return: Compiled click Command or None if there was an error
        """
        with open(plugin_script_path) as f:
            code = compile(f.read(), plugin_script_path, mode='exec')
            try:
                ns = {}
                eval(code, ns, ns)
                return ns[function_name]
            except Exception:
                logger.exception(f'Error compiling {plugin_script_path}')
                return None

    @classmethod
    def _cli_plugin_search(cls, workspace_path: str) -> Dict[str, WorkspaceEntryPointMetadata]:
        """
        Searches the workspace looking for pyproject.toml files with a cli.cli_plugins
        entry point

        :param workspace_path: path of the workspace to search
        :return: a dictionary of each entry point found
        """
        cli_plugins = {}
        print(f'About to search for plugins')
        for project_name in os.listdir(workspace_path):
            project_path = os.path.join(workspace_path, project_name)
            project_data_path = os.path.join(project_path, 'data')

            project_toml_path = os.path.join(project_path, 'pyproject.toml')
            if not os.path.exists(project_toml_path):
                print(f'Path does not have a pyproject.toml')
                continue

            with open(project_toml_path, "rb") as f:
                project_toml = tomllib.load(f)
                has_entrypoint = cls.check_for_entrypoint(CLI_PLUGINS_ENTRY_POINT, project_toml)
                has_workspace_entrypoint = cls.check_for_entrypoint(CLI_WORKSPACE_ONLY_PLUGINS_ENTRY_POINT, project_toml)
                if not has_entrypoint and not has_workspace_entrypoint:
                    logger.debug(f'the project {project_name} does not have entrypoint')
                    continue

                project_version = "5"
                if has_entrypoint:
                    found_entry_points = project_toml['project']['entry-points'][CLI_PLUGINS_ENTRY_POINT]
                    for entry_point_name, entry_point_value in found_entry_points.items():
                        entry_point_metadata = WorkspaceEntryPointMetadata.build(entry_point_name, entry_point_value, project_name, project_version, project_path, project_data_path)
                        cli_plugins[entry_point_metadata.name] = entry_point_metadata
                if has_workspace_entrypoint:
                    found_entry_points = project_toml['project']['entry-points'][CLI_WORKSPACE_ONLY_PLUGINS_ENTRY_POINT]
                    for entry_point_name, entry_point_value in found_entry_points.items():
                        entry_point_metadata = WorkspaceEntryPointMetadata.build(entry_point_name, entry_point_value, project_name, project_version, project_path, project_data_path)
                        cli_plugins[entry_point_metadata.name] = entry_point_metadata
        return cli_plugins

    @staticmethod
    def check_for_entrypoint(entrypoint_name: str, project_toml: Dict[str, Any]) -> bool:
        return 'project' in project_toml \
            and 'entry-points' in project_toml['project'] \
            and entrypoint_name in project_toml['project']['entry-points']

    @staticmethod
    def _absolute_script_path(project_path: str, script_name: str) -> Optional[str]:
        """
        Walks the filesystem below the project path to resolve the absolute path of
        the script specified in the entry point

        :param project_path: absolute path to the project
        :param script_name: name of the script somewhere in the project path
        :return: absolute path of the project
        """
        script_filename = f'{script_name}.py'
        exclude = {'.git', '.idea', '.ipynb_checkpoints', '__pycache__', '.pytest_cache', 'data'}
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in exclude]
            absolute_script_path = os.path.join(root, script_filename)
            if script_filename in files and os.path.exists(absolute_script_path):
                return absolute_script_path


