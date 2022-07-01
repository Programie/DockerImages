#! /bin/bash

set -e

usermod -u ${HTTPD_UID} www-data
groupmod -g ${HTTPD_GID} www-data

# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
	set -- apache2-foreground "$@"
fi

exec "$@"