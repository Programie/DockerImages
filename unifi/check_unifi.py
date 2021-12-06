#! /usr/bin/env python3
import json
import os
import re
import sys

from pyunifi.controller import Controller

username = os.getenv("UNIFI_API_USERNAME")
password = os.getenv("UNIFI_API_PASSWORD")
site_id = os.getenv("UNIFI_API_SITEID", "default")
expected_uplink_speed = os.getenv("UNIFI_UPLINK_SPEED")
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

        status = 0
        status_text = []

        if ap["state"] == 1:
            status = max(status, 0)
            status_text.append("Online")
        else:
            status = max(status, 2)
            status_text.append("Offline (!!)")

        uplink_speed = int(ap.get("uplink", {}).get("speed", 0))

        if expected_uplink_speed is not None:
            expected_uplink_speed = int(expected_uplink_speed)

            if uplink_speed != expected_uplink_speed:
                status = max(status, 2)
                status_text.append("Uplink: {} MBit/s but expected {} MBit/s (!!)".format(ap["uplink"]["speed"], expected_uplink_speed))

        client_count = len(clients)

        performance_data = {
            "rx_bytes": ap["rx_bytes"],
            "tx_bytes": ap["tx_bytes"],
            "uptime": ap["uptime"],
            "uplink_speed": uplink_speed,
            "clients": client_count
        }

        performance_data_array = []

        for key, value in performance_data.items():
            performance_data_array.append("{}={}".format(key, value))

        status_text.append("{} clients".format(client_count))
        status_text.append("Traffic: {} up / {} down".format(sizeof_fmt(ap["rx_bytes"]), sizeof_fmt(ap["tx_bytes"])))

        print("{} UniFi_Controller_{} {} {}".format(status, re.sub(r"\W+", "_", ap["name"]), "|".join(performance_data_array), ", ".join(status_text)))
    except BaseException as exception:
        print(exception, file=sys.stderr)
