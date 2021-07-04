#! /usr/bin/env python3

import os
import re
import sys

from pyunifi.controller import Controller

username = os.getenv("UNIFI_API_USERNAME")
password = os.getenv("UNIFI_API_PASSWORD")
site_id = os.getenv("UNIFI_API_SITEID", "default")
ssl_verify = os.path.join(os.getenv("CERTDIR"), os.getenv("CERTNAME"))


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Y", suffix)


controller = Controller(host="localhost", port=8443, username=username, password=password, site_id=site_id, ssl_verify=ssl_verify)

ap_clients = {}

for client in controller.get_clients():
    ap_mac = client["ap_mac"]

    if ap_mac not in ap_clients:
        ap_clients[ap_mac] = []

    ap_clients[ap_mac].append(client)

for ap in controller.get_aps():
    try:
        ap_mac = ap["mac"]

        if ap_mac in ap_clients:
            clients = ap_clients[ap_mac]
        else:
            clients = []

        if ap["state"] == 1:
            status = 0
            status_string = "Online"
        else:
            status = 2
            status_string = "Offline (!!)"

        client_count = len(clients)

        performance_data = {
            "rx_bytes": ap["rx_bytes"],
            "tx_bytes": ap["tx_bytes"],
            "uptime": ap["uptime"],
            "clients": client_count
        }

        performance_data_array = []

        for key, value in performance_data.items():
            performance_data_array.append("{}={}".format(key, value))

        status_text = [
            status_string,
            "{} clients".format(client_count),
            "Traffic: {} up / {} down".format(sizeof_fmt(ap["rx_bytes"]), sizeof_fmt(ap["tx_bytes"]))
        ]

        print("{} UniFi_Controller_{} {} {}".format(status, re.sub(r"\W+", "_", ap["name"]), "|".join(performance_data_array), ", ".join(status_text)))
    except BaseException as exception:
        print(exception, file=sys.stderr)
