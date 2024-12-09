#!/usr/bin/env python

import logging
import os
import click

from lab_partner.docker import DockerEnvironment
from lab_partner.rootless import RootlessContainer
from lab_partner.shell import ShellContainer


def loglevel() -> str:
    return os.environ.get('LOGLEVEL', 'INFO').upper()


logging.basicConfig(level=loglevel())
logger = logging.getLogger(__name__)


# DISPLAY = os.environ.get('DISPLAY', '')
# WORKSPACE = os.environ['LAB_WORKSPACE']
# WORKSPACE_DATA = os.path.join(WORKSPACE, 'data')
# NETWORK_NAME = 'lab'


@click.group(invoke_without_command=True)
@click.pass_context
def lab(ctx: click.Context):
    """
    Core Lab Management
    """
    if not ctx.invoked_subcommand:
        ctx.invoke(start)
        ctx.invoke(shell)
    else:
        click.echo(f"I am about to invoke {ctx.invoked_subcommand}")


@lab.command()
@click.option('--debug-rootless', is_flag=True, show_default=True, default=False, help='Turn debugging for Rootlesskit')
@click.option('--debug-bypass4netns', is_flag=True, show_default=True, default=False, help='Turn on debugging for Bypass4netns')
def start(debug_rootless: bool, debug_bypass4netns: bool):
    env = {
        'DOCKERD_ROOTLESS_ROOTLESSKIT_DEBUG': str(debug_rootless).lower(),
        'BYPASS4NETNS_DEBUG': str(debug_bypass4netns).lower()
    }
    rootless = RootlessContainer(DockerEnvironment(env))
    rootless.start()

    # docker_daemon_info = DockerDaemonInfo.build()
    # rootless = RootlessDockerContainer(docker_daemon_info)
    # docker_daemon_info = rootless.start(WORKSPACE)

    # cli_cmd = DockerRunBuilder(f'enclarify/lab-partner-cli:{lab_version()}')
    # cli_cmd.options() \
    #     .with_tty() \
    #     .with_env('LAB_DOCKER_SOCKET', docker_daemon_info.docker_internal_socket()) \
    #     .with_env('LAB_WORKSPACE', os.environ.get('LAB_WORKSPACE')) \
    #     .with_env('LAB_WORKSPACE', WORKSPACE) \
    #     .with_env('LAB_WORKSPACE_DATA', WORKSPACE_DATA) \
    #     .with_env('LAB_NETWORK_NAME', NETWORK_NAME) \
    #     .with_env('LAB_VERSION', lab_version()) \
    #     .with_home_dir_bind_mount('.gitconfig', '/opt/lab/home/.gitconfig') \
    #     .with_home_dir_bind_mount('.vim', '/opt/lab/home/.vim') \
    #     .with_home_dir_bind_mount('.vimrc', '/opt/lab/home/.vimrc') \
    #     .with_home_dir_bind_mount('.actrc', '/opt/lab/home/.actrc') \
    #     .with_home_dir_bind_mount('.aws', '/opt/lab/home/.aws') \
    #     .with_home_dir_bind_mount('.ssh', '/opt/lab/home/.ssh') \
    #     .with_bind_mount(WORKSPACE, WORKSPACE) \
    #     .with_bind_mount('/opt/lab/cicd/artifacts', '/opt/lab/cicd/artifacts') \
    #     .with_bind_mount(docker_daemon_info.docker_socket(), '/var/run/docker.sock') \
    #     .with_workdir(WORKSPACE)

    # cmd = shlex.split(cli_cmd.build())
    # os.execvpe(cmd[0], cmd, {'DOCKER_HOST': f'unix://{docker_daemon_info.docker_socket()}'})


@lab.command()
def stop():
    rootless = RootlessContainer(DockerEnvironment())
    rootless.stop()


@lab.command()
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'], case_sensitive=False), default='INFO')
def shell(log_level: str):
    env = {'LOG_LEVEL': log_level.upper()}
    shell = ShellContainer(RootlessContainer.rootless_env().put(env))
    shell.start()


if __name__ == '__main__':
    lab()
