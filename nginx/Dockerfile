FROM nginx

RUN apt-get update && \
    apt-get install -y --no-install-recommends bc openssl && \
    rm -rf /var/lib/apt/lists/*

COPY check_certs.sh /usr/local/bin/check_certs
COPY dhparam.pem /etc/ssl/dhparam.pem
COPY nginx.conf /etc/nginx/nginx.conf