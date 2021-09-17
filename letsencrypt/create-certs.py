#! /usr/bin/env python3

import os
import subprocess
import sys

letsencrypt_dir = "/etc/letsencrypt"
certs_dir = os.path.join(letsencrypt_dir, "live")
webroot = "/webroot"
email_address = os.environ["LETSENCRYPT_EMAIL"]

certs_requested = 0


def create_cert(domain_config: str):
    global certs_requested

    domain_config = domain_config.split(":")

    domains = domain_config[0]
    options = domain_config[1:]

    primary_domain = domains.split(":")[0]

    if not os.path.exists(os.path.join(certs_dir, primary_domain, "cert.pem")):
        command = ["certbot", "certonly", "--agree-tos", "--email", email_address, "--rsa-key-size", "4096", "-n"]

        if "dns_rfc2136" in options:
            command.append("--dns-rfc2136")
            command.append("--dns-rfc2136-credentials")
            command.append(os.path.join(letsencrypt_dir, "certbot-credentials.ini"))
        else:
            command.append("--webroot")
            command.append("-w")
            command.append(webroot)

        command.append("-d")
        command.append(domains)

        subprocess.run(command)

        certs_requested = 1


base_dir = os.path.dirname(__file__)
conf_file = os.path.join(base_dir, "create-certs.conf")

if not os.path.exists(conf_file):
    print("{}: Not found".format(conf_file), file=sys.stderr)
    exit(0)

with open(conf_file, "r") as file:
    for line in file.readlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        create_cert(line)

if certs_requested:
    subprocess.run([os.path.join(base_dir, "restart-container.sh"), os.environ["LETSENCRYPT_CONTAINER_RESTART_REQUEST"]])
