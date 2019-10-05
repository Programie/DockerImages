#!/usr/bin/python3

import os
import requests
import xmltodict

CHECK_MK_STATE_OK = 0
CHECK_MK_STATE_WARNING = 1
CHECK_MK_STATE_CRITICAL = 2
CHECK_MK_STATE_UNKNOWN = 3

check_name = os.getenv("OSCAM_CHECK_NAME", "oscam_cards")

url = "http://localhost:8888/oscamapi.html?part=status"

filtered = {}

xml = xmltodict.parse(requests.get(url).content)

for client in xml["oscam"]["status"]["client"]:
    if client["@type"] == "p" or client["@type"] == "r":
        filtered[client["@name"]] = client["connection"]["#text"]

cards_total = len(filtered)
cards_good = sum(1 for x in filtered.values() if x == "CARDOK" or x == "CONNECTED")
cards_bad = cards_total - cards_good

if cards_bad:
    state = CHECK_MK_STATE_CRITICAL
else:
    state = CHECK_MK_STATE_OK

print("{state} {check_name} count={cards_total}|good={cards_good}|bad={cards_bad} {cards_total} cards, {cards_bad} bad, {cards_good} good".format(state=state, check_name=check_name, cards_total=cards_total, cards_good=cards_good, cards_bad=cards_bad))
