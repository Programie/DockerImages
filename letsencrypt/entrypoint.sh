#! /bin/bash

case "$1" in
    docker-gen)
        docker-gen -watch -notify "/app/create-certs.py" /app/create-certs.tmpl /app/create-certs.conf
    ;;

    *)
        exec "$@"
    ;;
esac