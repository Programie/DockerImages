FROM debian:stretch

ENV DOCKER_GEN_VERSION 0.7.3
ENV DOCKER_GEN_DOWNLOAD_URL https://github.com/jwilder/docker-gen/releases/download/$DOCKER_GEN_VERSION/docker-gen-alpine-linux-amd64-$DOCKER_GEN_VERSION.tar.gz
ENV DOCKER_HOST unix:///tmp/docker.sock

RUN apt-get update && \
    apt-get install -y certbot curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL $DOCKER_GEN_DOWNLOAD_URL | tar xvz -C /usr/local/bin

COPY . /app

VOLUME ["/etc/letsencrypt", "/webroot"]

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["docker-gen"]