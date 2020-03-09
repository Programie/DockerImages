#! /usr/bin/env python3

import hashlib
import os
import pytz
import re

from datetime import datetime
from elasticsearch import Elasticsearch
from fritzconnection import FritzConnection

timezone = pytz.timezone(os.getenv("TZ", "UTC"))

es_client = Elasticsearch(hosts=os.getenv("ES_HOST", "elasticsearch"))
fritzbox_client = FritzConnection(address=os.getenv("FRITZ_HOST"))

index_prefix = os.getenv("ES_INDEX_PREFIX", "fritzbox")
index_date_format = os.getenv("ES_INDEX_DATE_FORMAT")

log_regex = re.compile(r"^([0-9\. :]+) (.*)$")

for line in fritzbox_client.call_action("DeviceInfo1", "GetDeviceLog")["NewDeviceLog"].split("\n"):
    match = log_regex.match(line)

    date_time = match.group(1)
    message = match.group(2)

    date = datetime.strptime(date_time, "%d.%m.%y %H:%M:%S")
    date = timezone.localize(date)

    doc_id = hashlib.sha1(line.encode("utf-8")).hexdigest()

    if index_date_format is None:
        index_name = index_prefix
    else:
        index_name = "-".join([index_prefix, date.strftime(index_date_format)])

    es_client.index(index_name, {
        "timestamp": date,
        "message": message
    }, id=doc_id)
