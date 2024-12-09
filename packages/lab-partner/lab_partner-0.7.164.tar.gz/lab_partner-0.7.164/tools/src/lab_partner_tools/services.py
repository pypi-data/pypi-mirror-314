#!/usr/bin/env python

import subprocess
import sys
import os
from pathlib import Path
from typing import Dict
import click
from click import ParamType, Option
from click.types import IntParamType


opensearch_data = os.path.join(workspace_data, 'opensearch', 'data')
opensearch_logs = os.path.join(workspace_data, 'opensearch', 'logs')

Path(opensearch_data).mkdir(parents=True, exist_ok=True)
Path(opensearch_logs).mkdir(parents=True, exist_ok=True)


env = {
    'PATH': path,
    'USER': user,
    'UID': uid,
    'GID': gid,
    'HOME': home,
    'DISPLAY': display,
    'WORKSPACE': workspace,
    'WORKSPACE_DATA': workspace_data,
    'NETWORK_NAME': network_name,
    'OPENSEARCH_DATA': opensearch_data,
    'OPENSEARCH_LOGS': opensearch_logs,
    'LAB_VERSION': lab_version
}


@click.group()
def services():
    pass


def expand_variables(content: str, replace_vars: Dict[str, str]):
    for k, v in replace_vars.items():
        content = content.replace('$' + k, v)
        content = content.replace('${' + k + '}', v)
    return content


def parse_image_name(image_name: str):
    if '/' in image_name:
        image_name_parts = image_name.split('/')
        registry_name = image_name_parts[0]
        root_image_name = image_name_parts[1].split(':')[0]
    else:
        registry_name = None
        root_image_name = image_name.split(':')[0]
    image_version = image_name.split(':')[1]
    return registry_name, root_image_name, image_version


def read_docker_compose_config() -> str:
    try:
        with open('/opt/lab-partner/docker-compose.yml', 'r') as config:
            prepared_config = expand_variables(config.read(), env)
        return prepared_config
    except subprocess.CalledProcessError as e:
        click.echo(e.stderr)
        sys.exit('Error parsing docker-compose.yml')


def exec_compose(compose_cmd: str, config: str):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Child process
        os.dup2(r, sys.stdin.fileno())
        os.close(r)
        os.close(w)
        up_command = f'docker-compose -f - {compose_cmd}'.split()
        os.execvp(up_command[0], up_command)
    else:
        # Parent process
        os.close(r)
        os.write(w, bytearray(config, 'utf-8'))
        os.close(w)
        pid, status = os.waitpid(pid, 0)


TRACING_SERVICES = 'proxy data-prepper otel-collector jaeger-agent opensearch-dashboards opensearch'
NOTEBOOK_SERVICES = 'proxy jupyter'


def start_services(services: str = ''):
    config = read_docker_compose_config()
    exec_compose(f'up -d --remove-orphans --force-recreate {services}', config)


def stop_services(services: str = ''):
    config = read_docker_compose_config()
    exec_compose(f'stop {services}', config)
    exec_compose(f'rm --force --stop -v {services}', config)


@services.command()
def start_all():
    start_services()


@services.command()
def stop_all():
    stop_services()


@services.command()
def start_tracing():
    start_services(TRACING_SERVICES)


@services.command()
def stop_tracing():
    stop_services(TRACING_SERVICES)


@services.command()
def start_notebook():
    start_services(NOTEBOOK_SERVICES)


@services.command()
def stop_notebook():
    stop_services(NOTEBOOK_SERVICES)


if __name__ == '__main__':
    services()
