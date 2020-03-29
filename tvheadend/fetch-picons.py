#! /usr/bin/env python3

import re
import requests
import subprocess
import sys

request = requests.get("https://api.github.com/repos/picons/picons/releases/latest")

request.raise_for_status()

for asset in request.json()["assets"]:
    if re.match(r"^snp-full\.220x132-190x102\.light\.on\.transparent_.*\.symlink\.tar\.xz$", asset["name"]):
        subprocess.check_call(["wget", "-O", "/tmp/picons.tar.xz", asset["browser_download_url"]], stdout=sys.stdout, stderr=sys.stderr)
        exit(0)

print("No matching Picons release found!", file=sys.stderr)
exit(1)
