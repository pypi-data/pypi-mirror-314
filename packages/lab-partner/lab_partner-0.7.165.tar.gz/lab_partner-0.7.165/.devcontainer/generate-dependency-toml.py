#!/usr/local/bin/python

import os
import tomli_w
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


template = """
[project]
name = 'dev-test-dependencies'
version = '1.0.0'
dependencies = []
[project.optional-dependencies]
dev = []
test = []
"""

os.mkdir('/tmp/deps')
with open('pyproject.toml', 'rb') as f:
    project_toml = tomllib.load(f)

deps_toml = tomllib.loads(template)
deps_toml['project']['dependencies'] = project_toml['project']['dependencies']
deps_toml['project']['optional-dependencies']['dev'] = project_toml['project']['optional-dependencies']['dev']
deps_toml['project']['optional-dependencies']['test'] = project_toml['project']['optional-dependencies']['test']

with open('/tmp/deps/pyproject.toml', 'wb') as f:
    tomli_w.dump(deps_toml, f)


