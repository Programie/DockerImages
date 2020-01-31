FROM python:3.8-buster

RUN pip install elasticsearch

COPY ./elastic-aggregate.py /elastic-aggregate.py

ENTRYPOINT ["/elastic-aggregate.py"]