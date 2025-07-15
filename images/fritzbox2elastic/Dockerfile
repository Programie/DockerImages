FROM python:3.8-bookworm

RUN pip install elasticsearch8 fritzconnection pytz

COPY write-logs.py /write-logs.py

ENTRYPOINT ["/write-logs.py"]
