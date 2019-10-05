#! /bin/bash

rsync -a /usr/src/minecraft/ ${MINECRAFT_DIR}/
rsync -a --delete /usr/src/minecraft/libraries/ ${MINECRAFT_DIR}/libraries/