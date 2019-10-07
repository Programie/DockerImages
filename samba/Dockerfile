FROM debian:buster

RUN apt-get update && \
    apt-get install -y samba && \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 139 445

ENTRYPOINT ["/entrypoint.sh"]

CMD ["smbd", "-F", "-S", "--no-process-group"]