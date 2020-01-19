FROM jacobalberty/unifi

RUN rm -f /etc/apt/sources.list.d/mongodb-org-3.4.list && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pyunifi && \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh
COPY ./check_unifi.py /usr/local/bin/check_unifi

ENTRYPOINT ["/entrypoint.sh"]

CMD ["unifi"]