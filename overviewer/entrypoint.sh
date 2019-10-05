#! /bin/bash

case "$1" in
    overviewer)
        shift
        exec overviewer.py "$@"
    ;;

    *)
        exec "$@"
    ;;
esac