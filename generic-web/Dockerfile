FROM php:7.4-apache

RUN echo "ServerTokens Prod" > /etc/apache2/conf-enabled/z-server-tokens.conf && \
    a2enmod rewrite && \
    docker-php-ext-install pdo_mysql && \
    mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"