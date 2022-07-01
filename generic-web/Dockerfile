ARG PHP_VERSION

ENV HTTPD_UID=33
ENV HTTPD_GID=33

FROM php:${PHP_VERSION}-apache

RUN echo "ServerTokens Prod" > /etc/apache2/conf-enabled/z-server-tokens.conf && \
    a2enmod rewrite && \
    docker-php-ext-install pdo_mysql && \
    mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" && \
    usermod -u ${HTTPD_UID} www-data && \
    groupmod -g ${HTTPD_GID} www-data