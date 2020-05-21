FROM debian:buster

RUN apt-get update && \
    apt-get install -y proftpd && \
    rm -rf /var/lib/apt/lists/*

CMD ["proftpd", "--nodaemon", "-c", "/etc/proftpd/proftpd.conf"]