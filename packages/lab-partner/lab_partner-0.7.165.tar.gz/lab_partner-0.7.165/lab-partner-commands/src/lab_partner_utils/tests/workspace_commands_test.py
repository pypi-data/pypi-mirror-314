import logging
from pathlib import Path
import os
os.environ['LAB_WORKSPACE'] = f'{str(Path(__file__).parent.resolve())}/fixtures/workspace_commands'

from click.testing import CliRunner
from lab_partner_utils.command_sets.workspace_entrypoint_commands import WorkspaceEntrypointCommands




def test_commands():
    print(f'{str(Path(__file__).parent.resolve())}/fixtures/workspace_commands')
    runner = CliRunner()
    result = runner.invoke(WorkspaceEntrypointCommands, ['hello'])
    print(result.stdout)
    assert result.exit_code == 0
    # print(result.stderr)