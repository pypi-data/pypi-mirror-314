import logging
import sys
if sys.version_info < (3, 8):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points
from typing import List, Optional
from click import Command, Context, MultiCommand
from . import CLI_PLUGINS_ENTRY_POINT


logger = logging.getLogger(__name__)


class MetadataEntrypointCommands(MultiCommand):
    """
    Searches installed python packages for CLI entry points
    and loads the specified functions as click Commands
    """

    def list_commands(self, ctx: Context) -> List[str]:
        """
        Generates list of subcommand names from installed packages for cli_plugins entry point

        :param ctx: current click context
        :return: list of subcommand names
        """
        plugin_names = []
        eps = entry_points().get(CLI_PLUGINS_ENTRY_POINT, [])
        for e in eps:
            plugin_names.append(e.name)
        return plugin_names

    def get_command(self, ctx: Context, plugin_name: str) -> Optional[Command]:
        """
        Builds a set of commands for an installed package with a CLI entry point
        and returns a click Command

        :param ctx: current click context
        :param plugin_name: name of the cli plugin in the installed package
        :return: Compiled click Command or None if there was an error
        """
        eps = entry_points().get(CLI_PLUGINS_ENTRY_POINT, [])
        for e in eps:
            if e.name == plugin_name:
                return e.load()