FROM debian:buster

ENV NAGFLUX_VERSION=0.4.1

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://github.com/Griesbacher/nagflux/releases/download/v${NAGFLUX_VERSION}/nagflux -o /usr/local/bin/nagflux && \
    chmod +x /usr/local/bin/nagflux && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/*

CMD ["nagflux", "-configPath", "/etc/nagflux.ini"]