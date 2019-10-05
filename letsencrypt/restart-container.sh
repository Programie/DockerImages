#! /bin/bash

container="$1"

if [[ -z ${container} ]]; then
    exit
fi

curl --unix-socket /tmp/docker.sock -X POST http://localhost/containers/${container}/restart