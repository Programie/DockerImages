#! /usr/bin/env python3

import hashlib
import os
import re

from datetime import datetime
from elasticsearch import Elasticsearch
from fritzconnection import FritzConnection

es_client = Elasticsearch(hosts=os.getenv("ES_HOST", "elasticsearch"))
fritzbox_client = FritzConnection(address=os.getenv("FRITZ_HOST"))

index_prefix = os.getenv("ES_INDEX", "fritzbox-")

log_regex = re.compile(r"^([0-9\. :]+) (.*)$")

for line in fritzbox_client.call_action("DeviceInfo1", "GetDeviceLog")["NewDeviceLog"].split("\n"):
    match = log_regex.match(line)

    date_time = match.group(1)
    message = match.group(2)

    date = datetime.strptime(date_time, "%d.%m.%y %H:%M:%S")

    doc_id = hashlib.sha1(line.encode("utf-8")).hexdigest()

    es_client.index("".join([index_prefix, date.strftime("%Y.%m")]), {
        "timestamp": date,
        "message": message
    }, id=doc_id)
