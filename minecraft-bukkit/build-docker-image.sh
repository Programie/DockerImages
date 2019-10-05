#! /bin/bash

set -e

docker build --pull --no-cache --build-arg MINECRAFT_VERSION=1.12.2 -t ${tag}:1.12.2 .
docker push ${tag}:1.12.2

docker build --pull --no-cache --build-arg MINECRAFT_VERSION=1.14.4 -t ${tag}:1.14.4 .
docker push ${tag}:1.14.4