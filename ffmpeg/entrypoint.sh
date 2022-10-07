#! /bin/bash

usermod -u ${FFMPEG_UID} ffmpeg > /dev/null
groupmod -g ${FFMPEG_GID} ffmpeg > /dev/null

exec gosu ffmpeg "$@"