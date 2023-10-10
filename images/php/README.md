# PHP

A base PHP Docker image providing Apache, the [Sury PHP repository](https://sury.org) as well as a simple installation script to install any PHP package provided by the Sury PHP repository.

## Usage

The following example will Install PHP 8.2 with curl, gd and pdo_mysql as additional PHP extensions.

```Dockerfile
FROM ghcr.io/programie/dockerimages/php

RUN install-php 8.2 curl gd pdo-mysql
```

## php.ini

By default, the php.ini is located at `/etc/php/${php_version}/apache2/php.ini` for Apache and `/etc/php/${php_version}/cli/php.ini` for the CLI.

Additionally, a symlink pointing to the config directory of the currently installed PHP version is created at `/etc/php/current`. In that way, it is possible to add php.ini files independently of the PHP version.

To share the same configuration between Apache and CLI, there is also a shared `global.ini` located at `/etc/php/current/global.ini`. This file is symlinked as `50-global.ini` into the conf.d folder of the Apache and CLI config directories (`/etc/php/current/apache2/conf.d/50-global.ini` and `/etc/php/current/cli/conf.d/50-global.ini`).

## Document root

The default document root is `/var/www/html` but can be changed using the environment variable `WEB_ROOT`.

## Timezone

The default timezone is `UTC` but can be changed using the environment variable `TZ`.