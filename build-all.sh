#! /bin/bash

set -e

script_dir=$(dirname $(realpath $0))

for dir in ${script_dir}/*; do
    if [[ ! -d ${dir} ]]; then
        continue
    fi

    image=$(basename ${dir})

    if [[ ${image} == "minecraft-bukkit" ]]; then
        continue
    fi

    echo -e "\033[1;32mBuilding image ${image}\033[0m"

    ${script_dir}/build-image.sh ${image}
done