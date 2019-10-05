#! /bin/bash

set -e

script_dir=$(dirname $(realpath $0))

for dir in ${script_dir}/*; do
    if [[ ! -d ${dir} ]]; then
        continue
    fi

    image=$(basename ${dir})
    tag="registry.gitlab.com/programie/dockerimages/${image}"

    echo -e "\033[1;32mBuilding image ${image}\033[0m"

    if [[ -e ${dir}/build-docker-image.sh ]]; then
        (cd ${dir} && tag=${tag} ./build-docker-image.sh)
        continue
    fi

    docker build --pull --no-cache -t ${tag} ${dir} && docker push ${tag}
done