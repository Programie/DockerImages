FROM debian:buster

ENV G10K_VERSION=0.6

RUN apt-get update && \
    apt-get install -y curl git unzip && \
    curl -sSL https://apt.puppetlabs.com/puppet6-release-stretch.deb -o puppet6-release.deb && \
    dpkg -i puppet6-release.deb && \
    rm puppet6-release.deb && \
    apt-get update && \
    apt-get install -y puppet-agent && \
    curl -sSL https://github.com/xorpaul/g10k/releases/download/v${G10K_VERSION}/g10k-linux-amd64.zip -o g10k-linux-amd64.zip && \
    unzip g10k-linux-amd64.zip && \
    mv g10k /usr/local/bin && \
    chmod +x /usr/local/bin/g10k && \
    rm g10k-linux-amd64.zip && \
    apt-get purge -y --auto-remove curl unzip && \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh
COPY ./g10k.yaml /etc/g10k.yaml

VOLUME ["/source", "/etc/puppetlabs/code"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["g10k-deploy"]