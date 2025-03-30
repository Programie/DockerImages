#! /bin/bash

usermod -u ${HTTPD_UID} www-data
groupmod -g ${HTTPD_GID} www-data
