#! /bin/bash

usermod --non-unique -u ${HTTPD_UID} www-data
groupmod --non-unique -g ${HTTPD_GID} www-data
