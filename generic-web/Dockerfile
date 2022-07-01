ARG PHP_VERSION

FROM php:${PHP_VERSION}-apache

ENV HTTPD_UID=33
ENV HTTPD_GID=33

COPY entrypoint.sh /entrypoint.sh

RUN echo "ServerTokens Prod" > /etc/apache2/conf-enabled/z-server-tokens.conf && \
    a2enmod rewrite && \
    docker-php-ext-install pdo_mysql && \
    mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

ENTRYPOINT ["/entrypoint.sh"]