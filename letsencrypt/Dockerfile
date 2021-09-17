FROM debian:buster

ARG TARGETARCH

ENV DOCKER_GEN_VERSION 0.7.7
ENV DOCKER_HOST unix:///tmp/docker.sock

RUN apt-get update && \
    apt-get install -y python3 certbot python3-certbot-dns-rfc2136 curl && \
    rm -rf /var/lib/apt/lists/*

RUN case ${TARGETARCH} in \
        amd64) ARCH="amd64";; \
        arm) ARCH="armhf";; \
        arm64) ARCH="arm64";; \
    esac; \
    curl -sSL https://github.com/nginx-proxy/docker-gen/releases/download/${DOCKER_GEN_VERSION}/docker-gen-linux-${ARCH}-${DOCKER_GEN_VERSION}.tar.gz | tar xvz -C /usr/local/bin

COPY . /app

VOLUME ["/etc/letsencrypt", "/webroot"]

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["docker-gen"]