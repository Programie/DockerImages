#! /bin/bash

case "$1" in
    g10k-deploy)
        g10k --config /etc/g10k.yaml
        /opt/puppetlabs/bin/puppet generate types
    ;;

    *)
        exec "$@"
    ;;
esac