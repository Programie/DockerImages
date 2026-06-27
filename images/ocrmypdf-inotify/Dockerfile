FROM alpine

RUN apk add ocrmypdf inotify-tools

COPY ocrmypdf-inotify-helper.sh /usr/local/bin/ocrmypdf-inotify-helper
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]
