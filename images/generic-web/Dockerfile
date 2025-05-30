FROM ghcr.io/programie/php-docker

ARG PHP_VERSION
ARG S6_OVERLAY_VERSION=3.2.0.2
ARG VOLTA_VERSION=2.0.2

LABEL org.opencontainers.image.version=$PHP_VERSION

ENV S6_KEEP_ENV=1
ENV HTTPD_UID=33
ENV HTTPD_GID=33
ENV PATH=/root/.volta/bin:$PATH

COPY --chmod=755 etc/cont-init.d /etc/cont-init.d

RUN apt-get update && apt-get install -y curl git xz-utils && \
    install-php ${PHP_VERSION} curl intl mbstring pdo-mysql xml && \
    a2enmod rewrite && \
    curl -o /usr/local/bin/composer https://getcomposer.org/download/latest-stable/composer.phar && \
    chmod +x /usr/local/bin/composer && \
    curl -L https://github.com/volta-cli/volta/releases/download/v${VOLTA_VERSION}/volta-${VOLTA_VERSION}-linux.tar.gz | tar -C /usr/local/bin -zxp && \
    curl -L https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz | tar -C / -Jxp && \
    curl -L https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz | tar -C / -Jxp

ENTRYPOINT ["/init"]
CMD ["apache2-foreground"]
