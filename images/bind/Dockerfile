FROM debian:buster

RUN apt-get update && \
    apt-get install -y bind9 && \
    rm -rf /var/lib/apt/lists/*

CMD ["named", "-g", "-u", "bind"]