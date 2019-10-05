#! /bin/bash

image="$1"

if [[ -z ${image} ]]; then
    echo "Usage: $0 <image name>"
    exit 1
fi

script_dir=$(dirname $(realpath $0))
dir="${script_dir}/${image}"
tag="registry.gitlab.com/programie/dockerimages/${image}"

if [[ -e ${dir}/build-docker-image.sh ]]; then
    (cd ${dir} && tag=${tag} ./build-docker-image.sh)
else
    docker build --pull --no-cache -t ${tag} ${dir} && docker push ${tag}
fi