FROM jbarlow83/ocrmypdf

RUN apt-get update && \
    apt-get install -y inotify-tools && \
    rm -rf /var/lib/apt/lists/*

COPY ocrmypdf-inotify-helper.sh /usr/local/bin/ocrmypdf-inotify-helper
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]