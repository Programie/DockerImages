FROM python

RUN pip install redis watchdog

COPY player-tracker.py /player-tracker.py

ENTRYPOINT ["/player-tracker.py"]