from unittest.mock import patch
from typing import Any, Dict, List, Optional

from lab_partner.rootless import LAB_ROOTLESS_DOCKERD, RootlessContainer


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_query_rootless_state(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'name': 'bob'}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert rootless._query_rootless_state(lambda c: 'bob' == c['name'])


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_query_rootless_state_missing(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'name': 'other'}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert not rootless._query_rootless_state(lambda c: 'bob' == c['name'])


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_query_rootless_state_empty(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = []
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert not rootless._query_rootless_state(lambda c: 'bob' == c['name'])


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_query_rootless_state_null(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = None
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert not rootless._query_rootless_state(lambda c: 'bob' == c['name'])


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_does_rootless_container_exist(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'Names': LAB_ROOTLESS_DOCKERD}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert rootless.does_rootless_container_exist()


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_does_rootless_container_not_exist(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'Names': 'bob'}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert not rootless.does_rootless_container_exist()


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_is_rootless_container_running(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'Names': LAB_ROOTLESS_DOCKERD, 'State': 'running'}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert rootless.is_rootless_container_running()


@patch('lab_partner.docker.daemon_info.DockerDaemonInfo')
def test_is_rootless_container_not_running(mock_docker_daemo_info):
    mock_docker_daemo_info.containers.return_value = [{'Names': LAB_ROOTLESS_DOCKERD, 'State': 'stopped'}]
    rootless = RootlessContainer(mock_docker_daemo_info)
    assert rootless.is_rootless_container_not_running()

