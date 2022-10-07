#! /bin/bash

exec gosu ${FFMPEG_UID}:${FFMPEG_GID} "$@"