#!/usr/bin/env python

import os
import pathlib

from ipykernel import kernelapp as app
import click


@click.command()
@click.option('--session-key', required=True)
@click.option('--heartbeat-port', required=True, type=int)
@click.option('--shell-port', required=True, type=int)
@click.option('--iopub-port', required=True, type=int)
@click.option('--stdin-port', required=True, type=int)
@click.option('--control-port', required=True, type=int)
@click.option('--debug', default=True)
def launch(session_key, heartbeat_port, shell_port, iopub_port, stdin_port, control_port, debug: bool):
    home = os.environ.get('HOME')
    uid = int(os.environ.get('UID'))
    gid = int(os.environ.get('GID'))
    pathlib.Path(home).mkdir(parents=True, exist_ok=True)
    os.chown(home, uid, gid)
    args = [
        f'--Session.key={session_key}',
        f'--ip=0.0.0.0',
        f'--hb={heartbeat_port}',
        f'--shell={shell_port}',
        f'--iopub={iopub_port}',
        f'--stdin={stdin_port}',
        f'--control={control_port}'
    ]
    if debug:
        args.append('--debug')
    app.launch_new_instance(argv=args)


if __name__ == '__main__':
    launch()
