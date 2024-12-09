#!/bin/bash

set -e

cmd=$1

version() {
  grep -Ei "^version" pyproject.toml | grep -Eio "([0-9]+\.[0-9]+\.[0-9]+)"
}

docker run -it --rm \
  -e USER=${USER} \
  -e HOME=${HOME} \
  -e DISPLAY=${DISPLAY} \
  -e WORKSPACE=${WORKSPACE} \
  enclarify/lab-partner:$(version) ${cmd}
