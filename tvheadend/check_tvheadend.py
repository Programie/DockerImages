#! /usr/bin/env python3
import os
import re

import requests
from requests.auth import HTTPDigestAuth


def scaled_value(value, scale, db_unit):
    max_value = 65535

    if scale == 1:  # Percentage
        calculated_value = value / max_value * 100
        return calculated_value, "{}%".format(round(calculated_value))
    elif scale == 2:  # dB
        calculated_value = value * 0.001
        return calculated_value, "{} {}".format(round(calculated_value, 1), db_unit)


CHECK_MK_STATE_OK = 0
CHECK_MK_STATE_WARNING = 1
CHECK_MK_STATE_CRITICAL = 2
CHECK_MK_STATE_UNKNOWN = 3

username = os.getenv("TVHEADEND_API_USERNAME")
password = os.getenv("TVHEADEND_API_PASSWORD")
timeout = os.getenv("TVHEADEND_API_TIMEOUT", 5)

check_name = os.getenv("TVHEADEND_CHECK_NAME", "Tvheadend_Input_{tuner}")

continuity_errors_critical = int(os.getenv("TVHEADEND_CHECK_CONTINUITY_ERRORS_CRITICAL", 100))
continuity_errors_warning = int(os.getenv("TVHEADEND_CHECK_CONTINUITY_ERRORS_WARNING", 50))

snr_signal_strength_percentage_critical = int(os.getenv("TVHEADEND_CHECK_SNR_SIGNAL_STRENGTH_PERCENTAGE_CRITICAL", 33))
snr_signal_strength_percentage_warning = int(os.getenv("TVHEADEND_CHECK_SNR_SIGNAL_STRENGTH_PERCENTAGE_WARNING", 66))

inputs_response = requests.get("http://localhost:9981/api/status/inputs", auth=HTTPDigestAuth(username, password), timeout=timeout)

inputs_response.raise_for_status()

inputs = inputs_response.json()["entries"]

for input_object in inputs:
    tuner_name = re.sub(r"\W+", "_", input_object["input"])

    snr = scaled_value(input_object["snr"], input_object["snr_scale"], "dB")
    signal_strength = scaled_value(input_object["signal"], input_object["signal_scale"], "dBm")
    bandwidth = input_object["bps"]
    continuity_errors = input_object["cc"]
    ec_bit = input_object["ec_bit"]
    tc_bit = input_object["tc_bit"]
    unc = input_object["unc"]
    transport_errors = input_object["te"]

    state = CHECK_MK_STATE_OK
    performance_data = {}
    details = []

    if tc_bit == 0:
        ber = input_object["ber"]
    else:
        ber = ec_bit / tc_bit

    if ber != 0:
        state = max(state, CHECK_MK_STATE_CRITICAL)
        details.append("BER = {} (!!)".format(ber))

    performance_data["ber"] = (ber, 1, 1)

    if unc != 0:
        # TODO: Uncorrected Blocks will always increase while scanning EPG... every day
        # state = max(state, CHECK_MK_STATE_CRITICAL)
        state = max(state, CHECK_MK_STATE_WARNING)
        details.append("Uncorrected Blocks = {} (!!)".format(unc))

    performance_data["unc"] = (unc, 1, 1)

    if transport_errors != 0:
        state = max(state, CHECK_MK_STATE_CRITICAL)
        details.append("Transport Errors = {} (!!)".format(transport_errors))

    performance_data["transport_errors"] = (transport_errors, 1, 1)

    performance_data["bandwidth"] = bandwidth

    if bandwidth:
        details.append("Bandwidth = {} kb/s".format(bandwidth / 1024))

    if continuity_errors > continuity_errors_critical:
        # TODO: Continuity Errors will always increase on switching mux and while scanning EPG... every day
        # state = max(state, CHECK_MK_STATE_CRITICAL)
        state = max(state, CHECK_MK_STATE_WARNING)
        details.append("Continuity Errors = {} (!!)".format(continuity_errors))
    elif continuity_errors > continuity_errors_warning:
        state = max(state, CHECK_MK_STATE_WARNING)
        details.append("Continuity Errors = {} (!)".format(continuity_errors))

    performance_data["continuity_errors"] = (continuity_errors, continuity_errors_warning, continuity_errors_critical)

    if snr is None:
        snr_value = 0
        snr_string = "N/A"
        performance_data["snr"] = 0
    else:
        snr_value, snr_string = snr

        # State calculation currently only possible if SNR is in percent (scale = 1)
        if input_object["snr_scale"] == 1:
            performance_data["snr"] = (snr_value, snr_signal_strength_percentage_warning, snr_signal_strength_percentage_critical)
            # TODO: SNR is currently only at ~24% which is bad but doesn't seem to have any impact right now
            # if snr_value <= snr_signal_strength_percentage_critical:
            #     state = max(state, CHECK_MK_STATE_CRITICAL)
            #     snr_string = "{} (!!)".format(snr_string)
            # elif snr_value <= snr_signal_strength_percentage_warning:
            #     state = max(state, CHECK_MK_STATE_WARNING)
            #     snr_string = "{} (!)".format(snr_string)
        else:
            performance_data["snr"] = snr_value

        details.append("SNR = {}".format(snr_string))

    if signal_strength is None:
        signal_strength_value = 0
        signal_strength_string = "N/A"
        performance_data["signal_strength"] = 0
    else:
        signal_strength_value, signal_strength_string = signal_strength

        # State calculation currently only possible if signal strength is in percent (scale = 1)
        if input_object["signal_scale"] == 1:
            performance_data["signal_strength"] = (signal_strength_value, snr_signal_strength_percentage_warning, snr_signal_strength_percentage_critical)
            if signal_strength_value <= snr_signal_strength_percentage_critical:
                state = max(state, CHECK_MK_STATE_CRITICAL)
                signal_strength_string = "{} (!!)".format(signal_strength_string)
            elif signal_strength_value <= snr_signal_strength_percentage_warning:
                state = max(state, CHECK_MK_STATE_WARNING)
                signal_strength_string = "{} (!)".format(signal_strength_string)
        else:
            performance_data["signal_strength"] = signal_strength_value

        details.append("Signal Strength = {}".format(signal_strength_string))

    if "stream" in input_object:
        active_stream = input_object["stream"]
    else:
        active_stream = "Stream inactive"

    performance_data_string = []

    for key, value in performance_data.items():
        if type(value) == tuple:
            performance_data_string.append("{}={}".format(key, ";".join(map(str, value))))
        else:
            performance_data_string.append("{}={}".format(key, value))

    if len(details):
        details_string = "({})".format(", ".join(details))
    else:
        details_string = ""

    print("{state} {check_name} {performance_data} {active_stream} {details}".format(state=state, check_name=check_name.format(tuner=tuner_name), performance_data="|".join(performance_data_string), active_stream=active_stream, details=details_string))
