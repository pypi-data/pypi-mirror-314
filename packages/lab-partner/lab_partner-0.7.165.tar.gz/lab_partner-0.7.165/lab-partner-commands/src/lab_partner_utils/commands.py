import json
import os
from pathlib import PurePath
from collections import namedtuple
from typing import Optional, Dict

import click
from datetime import datetime

from docker import APIClient
from pytz import timezone


eastern = timezone('US/Eastern')
NETWORK_NAME = os.environ.get('NETWORK_NAME')
USER = os.environ.get('USER')
UID = int(os.environ.get('UID'))
GID = int(os.environ.get('GID'))
DOCKER_GID = int(os.environ.get('DOCKER_GID'))
TRACING_HOST = os.environ.get('TRACING_HOST')
TRACING_PORT = os.environ.get('TRACING_PORT')

# The kernel image where this will be used is supplied by the user so
# we need to use /tmp for the HOME path because it will be writable
home_path_parts = list(PurePath(os.environ.get('HOME')).parts)
HOME = str(PurePath('/tmp').joinpath(*home_path_parts[2:]))


KernelConnection = namedtuple('KernelConnection', ['key', 'control_port', 'shell_port', 'stdin_port', 'hb_port', 'iopub_port'])


__all__ = ['lab_start_kernel', 'lab_start_kernel_impl']


def parse_kernel_connection(connection: str) -> KernelConnection:
    with open(connection, 'r') as cxn_fp:
        connection_params = json.load(cxn_fp)

    return KernelConnection(
        key=connection_params['key'].encode('utf-8'),
        control_port=connection_params['control_port'],
        shell_port=connection_params['shell_port'],
        stdin_port=connection_params['stdin_port'],
        hb_port=connection_params['hb_port'],
        iopub_port=connection_params['iopub_port']
    )


class DockerRunOptions(object):
    def __init__(self):
        self.options = set()

    def with_option(self, option: str) -> 'DockerRunOptions':
        self.options.add(option)
        return self

    def with_http(self, hostname: str, port: int) -> 'DockerRunOptions':
        self.options.add('-l traefik.enable=true')
        self.options.add(f'-l traefik.http.routers.{hostname}.rule=Host(`{hostname}`)')
        self.options.add(f'-l traefik.http.services.{hostname}.loadbalancer.server.port={port}')
        return self

    def with_gpu(self) -> 'DockerRunOptions':
        self.options.add('--gpus all')
        self.options.add('-e NVIDIA_DRIVER_CAPABILITIES=video,compute,utility')
        return self

    def with_privileged(self) -> 'DockerRunOptions':
        self.options.add('--privileged')
        return self

    def with_add_devices(self) -> 'DockerRunOptions':
        self.options.add('-v /dev:/dev')
        self.with_privileged()
        return self

    def with_display(self) -> 'DockerRunOptions':
        display = os.environ.get('DISPLAY')
        self.options.add(f'-e DISPLAY={display}')
        self.options.add('-e QT_X11_NO_MITSHM=1')
        self.options.add('-v /tmp/.X11-unix:/tmp/.X11-unix:ro')
        return self

    def with_shared_memory(self) -> 'DockerRunOptions':
        self.options.add(f'--ipc=host')
        self.options.add('--ulimit memlock=-1:-1')
        self.options.add('--ulimit stack=-1:-1')
        self.with_add_devices()
        return self

    def build(self):
        return ' '.join(self.options)


def lab_start_kernel(connection: str, registry_name: str, options: DockerRunOptions):
    pass


def lab_start_kernel_impl(connection: str, registry_name: str, project_name: str,
                          project_version: str, project_path: str, options: DockerRunOptions):
    options_str = options.build()
    cxn = parse_kernel_connection(connection)
    project_data = os.path.join(project_path, 'data')
    kernel_image = f"{registry_name}/{project_name}:{project_version}"
    cmd = f'docker run --rm --init \
            {options_str} \
            -e USER={USER} \
            -e HOME={HOME} \
            -e UID={UID} \
            -e GID={GID} \
            -e OTEL_EXPORTER_JAEGER_AGENT_HOST={TRACING_HOST} \
            -e OTEL_EXPORTER_JAEGER_AGENT_PORT={TRACING_PORT} \
            -e PROJECT_WORKSPACE={project_path} \
            -e PROJECT_DATA={project_data} \
            -v {project_path}:{project_path} \
            -v {project_data}:{project_data} \
            -w {project_path} \
            --user {UID}:{GID} \
            --network=container:jupyter \
            --name {project_name}-kernel-{ datetime.now(eastern).strftime("%Y-%m-%d__%H-%M-%S") } \
            {kernel_image} \
            launch-kernel \
                --session-key={cxn.key} \
                --heartbeat-port={cxn.hb_port} \
                --shell-port={cxn.shell_port} \
                --iopub-port={cxn.iopub_port} \
                --stdin-port={cxn.stdin_port} \
                --control-port={cxn.control_port}'.split()
    click.echo(f'Starting kernel: {cmd}')
    os.execvp(cmd[0], cmd)


def lab_build_image(registry_name: str, nocache: bool = False, build_args: Optional[Dict[str, str]] = None):
    pass


def lab_build_image_impl(registry_name: str, project_name: str, project_version: str,
                         project_path: str, nocache: bool = False, build_args: Optional[Dict[str, str]] = None):
    image_name = f"{registry_name}/{project_name}:{project_version}"
    client = APIClient(base_url='unix://var/run/docker.sock')
    logs = client.build(
        decode=True,
        nocache=nocache,
        path=project_path,
        tag=image_name,
        rm=True,
        buildargs=build_args
    )
    for chunk in logs:
        if 'stream' in chunk:
            for line in chunk['stream'].splitlines():
                click.echo(line)


def lab_run_image(registry_name: str, project_name: str,
                  project_version: str, project_path: str, options: DockerRunOptions):
    pass


def lab_run_image_impl(registry_name: str, project_name: str,
                       project_version: str, project_path: str, options: DockerRunOptions):
    options_str = options.build()
    project_data = os.path.join(project_path, 'data')
    kernel_image = f"{registry_name}/{project_name}:{project_version}"
    cmd = f'docker run --rm --init \
            {options_str} \
            -e USER={USER} \
            -e HOME={HOME} \
            -e UID={UID} \
            -e GID={GID} \
            -e OTEL_EXPORTER_JAEGER_AGENT_HOST={TRACING_HOST} \
            -e OTEL_EXPORTER_JAEGER_AGENT_PORT={TRACING_PORT} \
            -e PROJECT_WORKSPACE={project_path} \
            -e PROJECT_DATA={project_data} \
            -v {project_path}:{project_path} \
            -v {project_data}:{project_data} \
            -w {project_path} \
            --user {UID}:{GID} \
            --network=container:jupyter \
            --name {project_name}-kernel-{datetime.now(eastern).strftime("%Y-%m-%d__%H-%M-%S")} \
            {kernel_image} \
            launch-kernel \
                --session-key={cxn.key} \
                --heartbeat-port={cxn.hb_port} \
                --shell-port={cxn.shell_port} \
                --iopub-port={cxn.iopub_port} \
                --stdin-port={cxn.stdin_port} \
                --control-port={cxn.control_port}'.split()
    click.echo(f'Running app: {cmd}')
    os.execvp(cmd[0], cmd)

    # "OTEL_EXPORTER_JAEGER_ENDPOINT": "",
    # "OTEL_EXPORTER_JAEGER_AGENT_HOST": "",
    # "OTEL_EXPORTER_JAEGER_AGENT_PORT": "",
    # "OTEL_EXPORTER_JAEGER_AGENT_SPLIT_OVERSIZED_BATCHES": "",
    # "OTEL_EXPORTER_JAEGER_TIMEOUT": "",

