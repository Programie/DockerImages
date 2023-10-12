# Generic Web

A Docker image for providing a generic web server using Apache and PHP.

The PHP version to use must be specified using the build argument `PHP_VERSION` (i.e. `PHP_VERSION=8.2`).

The image contains commonly used PHP extensions like `curl` or `pdo-mysql`, some additional Debian packages like `curl` or `git` as well as the latest version of [Composer](https://getcomposer.org).

## Customization

As this image is based on my [php image](../php), any customization options from that image also apply to this image.

Additionally, it is possible to change the user and group IDs of the `www-data` user which Apache uses. They can be changed by setting the environment variables `HTTPD_UID` and/or `HTTPD_GID` to different IDs.