#! /bin/bash

case "$1" in
    run)
        inotifywait \
            --format "%w/%f" \
            --event "${INOTIFY_EVENT:-close_write}" \
            --recursive \
            --monitor \
            /workdir | xargs -I{} ocrmypdf-inotify-helper {}
    ;;

    *)
        exec "$@"
    ;;
esac