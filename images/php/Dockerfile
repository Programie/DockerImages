FROM debian:bookworm

ENV APACHE_CONFDIR=/etc/apache2
ENV APACHE_ENVVARS=/etc/apache2/envvars
ENV WEB_ROOT=/var/www/html
ENV TZ=UTC

COPY apt.gpg /usr/share/keyrings/deb.sury.org-php.gpg

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends lsb-release ca-certificates apache2; \
    echo "deb [signed-by=/usr/share/keyrings/deb.sury.org-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list; \
    rm -rf /var/lib/apt/lists/*; \
    . ${APACHE_ENVVARS}; \
    for dir in \
        "$APACHE_LOCK_DIR" \
        "$APACHE_RUN_DIR" \
        "$APACHE_LOG_DIR" \
    ; do \
        rm -rvf "$dir"; \
        mkdir -p "$dir"; \
        chown "$APACHE_RUN_USER:$APACHE_RUN_GROUP" "$dir"; \
    done; \
    rm -rf ${APACHE_CONFDIR}/conf-enabled; \
    mkdir ${APACHE_CONFDIR}/conf-enabled; \
    ln -sfT /dev/stderr ${APACHE_LOG_DIR}/error.log; \
    ln -sfT /dev/stdout ${APACHE_LOG_DIR}/access.log; \
    ln -sfT /dev/stdout ${APACHE_LOG_DIR}/other_vhosts_access.log; \
    rm -rf /var/www/html; \
    mkdir /var/www/html; \
    chown -R www-data:www-data /var/www/html

COPY config/apache2.conf ${APACHE_CONFDIR}/conf-enabled/10-docker.conf
COPY config/apache2-vhost.conf ${APACHE_CONFDIR}/sites-enabled/000-default.conf
COPY config/php.ini /etc/php/docker.ini
COPY bin/ /usr/local/bin/

WORKDIR ${WEB_ROOT}

EXPOSE 80

CMD ["apache2-foreground"]