FROM linuxserver/tvheadend

RUN apk add python3 py3-pip && \
    pip3 install requests

COPY fetch-picons.py /opt/fetch-picons.py
COPY push-notification.sh /opt/push-notification.sh
COPY check_tvheadend.py /usr/local/bin/check_tvheadend

RUN /opt/fetch-picons.py && \
    mkdir /usr/share/picons && \
    cd /usr/share/picons && \
    tar --strip-components=1 -xf /tmp/picons.tar.xz && \
    rm /tmp/picons.tar.xz