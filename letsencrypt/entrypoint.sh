#! /bin/bash

case "$1" in
    docker-gen)
        docker-gen -watch -notify "/app/create-certs.sh" /app/create-certs.tmpl /app/create-certs.conf
    ;;

    *)
        exec "$@"
    ;;
esac