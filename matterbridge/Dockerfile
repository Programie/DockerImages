FROM debian:stretch

ENV MATTERBRIDGE_VERSION=1.16.1

RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    curl -sSL -o /usr/local/bin/matterbridge https://github.com/42wim/matterbridge/releases/download/v${MATTERBRIDGE_VERSION}/matterbridge-${MATTERBRIDGE_VERSION}-linux-64bit && \
    chmod +x /usr/local/bin/matterbridge && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/matterbridge"]
CMD ["-conf", "/etc/matterbridge.toml"]