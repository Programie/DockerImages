#! /bin/bash

image="$1"
tag="$2"
multiarch="$3"

if [[ -z ${image} ]]; then
    echo "Usage: $0 <image name> [<tag>] [multiarch]"
    exit 1
fi

shift
shift
shift

if [[ -z ${tag} ]]; then
    tag="latest"
fi

if [[ ${multiarch} == "multiarch" ]]; then
    platform="linux/amd64,linux/arm/v7"
else
    platform="linux/amd64"
fi

script_dir=$(dirname $(realpath $0))
dir="${script_dir}/${image}"
full_tag="registry.gitlab.com/programie/dockerimages/${image}:${tag}"

docker build build --pull --push --no-cache "$@" --tag "${full_tag}" --platform "${platform}" "${dir}"