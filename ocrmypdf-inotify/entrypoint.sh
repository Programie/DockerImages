#! /bin/bash

case "$1" in
    run)
        inotifywait \
            --format "%w/%f" \
            --event close_write \
            --event moved_to \
            --recursive \
            --monitor \
            /workdir | xargs -I{} ocrmypdf-inotify-helper {}
    ;;

    *)
        exec "$@"
    ;;
esac