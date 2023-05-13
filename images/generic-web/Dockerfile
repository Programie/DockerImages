ARG PHP_VERSION

FROM php:${PHP_VERSION}-apache

LABEL org.opencontainers.image.version=$PHP_VERSION

ENV HTTPD_UID=33
ENV HTTPD_GID=33

COPY entrypoint.sh /entrypoint.sh

RUN echo "ServerTokens Prod" > /etc/apache2/conf-enabled/z-server-tokens.conf && \
    a2enmod rewrite && \
    docker-php-ext-install pdo_mysql sockets && \
    mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" && \
    curl -o /usr/local/bin/composer https://getcomposer.org/download/latest-stable/composer.phar && \
    chmod +x /usr/local/bin/composer

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]