FROM python:3.8-bookworm

RUN pip install elasticsearch8

COPY elastic-aggregate.py /elastic-aggregate.py

ENTRYPOINT ["/elastic-aggregate.py"]
