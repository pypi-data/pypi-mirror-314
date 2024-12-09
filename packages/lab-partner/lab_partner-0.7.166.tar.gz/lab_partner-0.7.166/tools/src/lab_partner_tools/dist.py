#!/usr/bin/env python
import os
import subprocess

import click


LAB_DIST = os.environ['LAB_DIST']


def print_output(rs):
    if rs.returncode == 0:
        click.echo(rs.stdout.decode('utf-8'))
    else:
        click.echo(rs.stderr.decode('utf-8'))


@click.group()
def dist():
    pass


@dist.command()
def pypi():
    rs = subprocess.run(['twine', 'upload', '--verbose', f'{LAB_DIST}/init/*'], capture_output=True)
    print_output(rs)
    rs = subprocess.run(['twine', 'upload', f'{LAB_DIST}/utils/*'], capture_output=True)
    print_output(rs)


@dist.command()
def test_pypi():
    rs = subprocess.run(['twine', 'upload', '--repository', 'testpypi', f'{LAB_DIST}/init/*'], capture_output=True)
    print_output(rs)
    rs = subprocess.run(['twine', 'upload', '--repository', 'testpypi', f'{LAB_DIST}/utils/*'], capture_output=True)
    print_output(rs)


if __name__ == '__main__':
    dist()
