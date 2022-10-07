FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY record-stream.sh /usr/local/bin/record-stream