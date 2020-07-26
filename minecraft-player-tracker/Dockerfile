FROM python:3.8-buster

RUN pip install elasticsearch watchdog

COPY player-tracker.py /player-tracker.py

ENTRYPOINT ["/player-tracker.py"]