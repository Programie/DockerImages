FROM ghcr.io/programie/dockerimages/php

ARG PHP_VERSION

LABEL org.opencontainers.image.version=$PHP_VERSION

ENV HTTPD_UID=33
ENV HTTPD_GID=33

COPY entrypoint.sh /entrypoint.sh

RUN apt-get update && apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/* && \
    install-php ${PHP_VERSION} intl pdo-mysql && \
    a2enmod rewrite && \
    curl -o /usr/local/bin/composer https://getcomposer.org/download/latest-stable/composer.phar && \
    chmod +x /usr/local/bin/composer

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]