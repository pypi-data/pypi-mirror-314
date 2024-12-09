import os
from pytest import fixture
from lab_partner.docker_old.run_builder import DockerRunOptions


def assert_only_one(options: DockerRunOptions, option_prefix: str) -> None:
    assert options.build().count(option_prefix) == 1


@fixture(scope="session", autouse=True)
def setup_env():
    os.environ['HOME'] = '/home/me'
    os.environ['USER'] = 'me'
    yield "run test"
    del os.environ['HOME']
    del os.environ['USER']


def test_init_option():
    options = DockerRunOptions()
    option_prefix = '--init'
    options.with_init()
    assert_only_one(options, option_prefix)
    options.with_init()
    assert_only_one(options, option_prefix)


def test_remove_on_exit_option():
    options = DockerRunOptions()
    option_prefix = '--rm'
    options.with_remove_on_exit()
    assert_only_one(options, option_prefix)
    options.with_remove_on_exit()
    assert_only_one(options, option_prefix)


def test_name_option():
    options = DockerRunOptions()
    option_prefix = '--name'
    option_value = 'bob'
    options.with_name(option_value)
    assert_only_one(options, option_prefix)
    option_value = 'sue'
    options.with_name(option_value)
    assert_only_one(options, option_prefix)


def test_hostname_option():
    options = DockerRunOptions()
    option_prefix = '--hostname'
    option_value = 'bob'
    options.with_hostname(option_value)
    assert_only_one(options, option_prefix)
    option_value = 'sue'
    options.with_hostname(option_value)
    assert_only_one(options, option_prefix)


def test_user_option():
    options = DockerRunOptions()
    option_prefix = '--user'
    option_value1 = 1
    option_value2 = 1
    options.with_user(option_value1, option_value2)
    assert_only_one(options, option_prefix)
    option_value1 = 2
    option_value2 = 2
    options.with_user(option_value1, option_value2)
    assert_only_one(options, option_prefix)


