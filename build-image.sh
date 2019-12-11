#! /bin/bash

image="$1"
tag="$2"

if [[ -z ${image} ]]; then
    echo "Usage: $0 <image name> [<tag>]"
    exit 1
fi

shift
shift

if [[ -z ${tag} ]]; then
    tag="latest"
fi

script_dir=$(dirname $(realpath $0))
dir="${script_dir}/${image}"
full_tag="registry.gitlab.com/programie/dockerimages/${image}:${tag}"

docker build --pull --no-cache "$@" -t ${full_tag} ${dir} && docker push ${full_tag}