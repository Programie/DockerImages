FROM linuxserver/tvheadend

RUN apk add python3 py3-pip && \
    pip3 install requests

COPY push-notification.sh /opt/push-notification.sh
COPY check_tvheadend.py /usr/local/bin/check_tvheadend