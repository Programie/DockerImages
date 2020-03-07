FROM linuxserver/tvheadend

ENV PICONS_TAR_URL=https://github.com/picons/picons/releases/download/2/snp-full.220x132-190x102.light.on.transparent_2020-03-06--10-21-07.symlink.tar.xz

RUN apk add python3 && \
    pip3 install --upgrade pip && \
    pip3 install requests

RUN wget -O /tmp/picons.tar.xz ${PICONS_TAR_URL} && \
    mkdir /usr/share/picons && \
    cd /usr/share/picons && \
    tar --strip-components=1 -xf /tmp/picons.tar.xz && \
    rm /tmp/picons.tar.xz

COPY push-notification.sh /opt/push-notification.sh
COPY check_tvheadend.py /usr/local/bin/check_tvheadend