#! /bin/bash

rsync -av /usr/src/minecraft/ ${MINECRAFT_DIR}/
rsync -av --delete /usr/src/minecraft/libraries/ ${MINECRAFT_DIR}/libraries/