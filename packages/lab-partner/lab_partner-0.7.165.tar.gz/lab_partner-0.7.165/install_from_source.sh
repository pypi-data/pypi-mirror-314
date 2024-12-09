#!/bin/bash

set -e

. ./build.sh

echo "Copying lab-partner wheel from docker image"
container_id=$(docker create enclarify/lab-partner-packages:$(version))
docker cp ${container_id}:/opt/lab/dist/init/lab_partner-$(version)-py3-none-any.whl - > /tmp/lab_partner-$(version)-py3-none-any.whl
docker rm -f ${container_id}

echo "Pushing Docker images to Docker Hub"
docker push enclarify/lab-partner-cli:$(version)
#docker push enclarify/lab-partner-jupyter:$(version)

echo "Installing lab-partner on host"
pip3 install --upgrade --force-reinstall /tmp/lab_partner-$(version)-py3-none-any.whl

#git add -A
#git commit -m wip
#git tag -a 0.7.58
#git push --tags
#pip3 install --upgrade --force-reinstall lab_partner