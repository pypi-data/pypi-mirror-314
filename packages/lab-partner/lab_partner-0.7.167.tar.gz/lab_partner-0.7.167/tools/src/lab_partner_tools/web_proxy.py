import sys

import click
from lab_partner_utils.cli_command_factory import WorkspaceEntryPointMetadata
from lab_partner_utils.utils import start_services, stop_services, read_env


if sys.version_info >= (3, 12):
    from importlib import resources
else:
    import importlib_resources as resources


data_text = resources.files('lab_partner_tools.data').joinpath('data1.txt').read_text()


WORKSPACE_METADATA_SHIM = WorkspaceEntryPointMetadata('', '', '', '', 'lab', cli_root, os.path.join(cli_root, 'data'))
WEB_SERVICE = 'proxy'



@click.group()
def web_proxy():
    pass


@web_proxy.command()
@click.option('--listen-on-high-port', is_flag=True, show_default=True, default=False, help='Listen on port 8600 instead of 80. Useful if sitting behind another proxy already')
def start_web(listen_on_high_port: bool) -> None:
    """
    Start the reverse proxy webserver
    """
    env_override = {}
    if listen_on_high_port:
        env_override['TRAEFIK_LISTEN_PORT'] = '8600'
    start_services(WORKSPACE_METADATA_SHIM, ENVIRONMENT_PATH, services=WEB_SERVICE, env_override=env_override)


if __name__ == '__main__':
    web_proxy()
