FROM python:3.8-buster

RUN pip install elasticsearch telethon

COPY ./client.py /client.py

VOLUME /sessions

ENTRYPOINT ["/client.py"]