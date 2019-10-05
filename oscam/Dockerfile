FROM linuxserver/oscam

RUN apk add python3 && \
    pip3 install --upgrade pip && \
    pip3 install requests xmltodict

COPY check_oscam.py /usr/local/bin/check_oscam