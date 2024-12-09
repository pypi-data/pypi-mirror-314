#!/usr/bin/env python

import sys
import logging

from click import CommandCollection

from .command_sets.metadata_entrypoint_commands import MetadataEntrypointCommands
from .command_sets.workspace_entrypoint_commands import WorkspaceEntrypointCommands


logger = logging.getLogger(__name__)


plugin_commands = MetadataEntrypointCommands()
workspace_commands = WorkspaceEntrypointCommands()
cli = CommandCollection(sources=[workspace_commands, plugin_commands])


if __name__ == '__main__':
    cli()
