FROM php:cli

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    git clone https://github.com/carlos22/carddav2fb.git /opt/carddav2fb && \
    apt-get purge -y --auto-remove git; \
    rm -rf /var/lib/apt/lists/*

COPY selfcoders-ca.crt /usr/local/share/ca-certificates

RUN update-ca-certificates

COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /opt/carddav2fb

ENTRYPOINT ["/entrypoint.sh"]
CMD ["carddav2fb"]