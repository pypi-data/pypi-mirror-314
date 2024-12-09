#!/bin/bash

set -e

version() {
  grep -Ei "^#version" pyproject.toml | grep -Eio "([0-9]+\.[0-9]+\.[0-9]+)"
}

LAB_VERSION=$(version)

docker build \
  --target lab_packages \
  --progress=plain \
  --no-cache \
  --build-arg LAB_VERSION=${LAB_VERSION} \
  -t enclarify/lab-partner-packages:${LAB_VERSION}  .

docker build \
  --target lab_cli \
  --progress=plain \
  --no-cache \
  --build-arg LAB_VERSION=${LAB_VERSION} \
  -t enclarify/lab-partner-cli:${LAB_VERSION}  .

#docker build \
#  --target lab_jupyter \
#  --progress=plain \
#  --no-cache \
#  -t enclarify/lab-partner-jupyter:${LAB_VERSION}  .

#docker build \
#  --target data-prepper \
#  -t enclarify/data-prepper:1.0.0 \
#  environments/local
#
#docker build \
#  --target opentelemetry-collector \
#  -t enclarify/opentelemetry-collector:0.31.0 \
#  environments/local
