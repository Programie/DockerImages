FROM debian:bullseye

ENV G10K_VERSION=0.9.8
ENV PUPPET_VERSION=8

LABEL org.opencontainers.image.version=${G10K_VERSION}

RUN apt-get update && \
    apt-get install -y curl git unzip && \
    curl -sSL https://apt.puppetlabs.com/puppet${PUPPET_VERSION}-release-bullseye.deb -o puppet-release.deb && \
    dpkg -i puppet-release.deb && \
    rm puppet-release.deb && \
    apt-get update && \
    apt-get install -y puppet-agent && \
    curl -sSL https://github.com/xorpaul/g10k/releases/download/v${G10K_VERSION}/g10k-linux-amd64.zip -o g10k-linux-amd64.zip && \
    unzip g10k-linux-amd64.zip && \
    mv g10k /usr/local/bin && \
    chmod +x /usr/local/bin/g10k && \
    rm g10k-linux-amd64.zip && \
    apt-get purge -y --auto-remove curl unzip && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
COPY g10k.yaml /etc/g10k.yaml

VOLUME ["/source", "/etc/puppetlabs/code"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["g10k-deploy"]