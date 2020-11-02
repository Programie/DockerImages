FROM jbarlow83/ocrmypdf

RUN apt-get update && \
    apt-get install -y incron; \
    rm -rf /var/lib/apt/lists/*

RUN echo '/workdir IN_CLOSE_WRITE,IN_NO_LOOP ocrmypdf-inotify-helper $@ $#' > /etc/incron.d/ocrmypdf

COPY ./ocrmypdf-inotify-helper.sh /usr/local/bin/ocrmypdf-inotify-helper

ENTRYPOINT ["incrond"]
CMD ["--foreground"]