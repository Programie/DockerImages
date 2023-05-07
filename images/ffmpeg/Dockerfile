FROM debian:bullseye

ARG GOSU_VERSION=1.14

ENV FFMPEG_UID=1000
ENV FFMPEG_GID=1000

RUN apt-get update && \
    apt-get install -y ffmpeg wget && \
    rm -rf /var/lib/apt/lists/* && \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-amd64" && \
    chmod +x /usr/local/bin/gosu

COPY entrypoint.sh /entrypoint.sh
COPY record-stream.sh /usr/local/bin/record-stream

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]