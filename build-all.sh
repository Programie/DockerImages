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

for minecraft_version in 1.12.2 1.14.4 1.15.2 1.16.5; do
    ${script_dir}/build-image.sh minecraft-bukkit ${minecraft_version} amd64 --build-arg MINECRAFT_VERSION=${minecraft_version}
done