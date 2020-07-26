#! /usr/bin/env python3

import json
import os

import time
from fnmatch import fnmatch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent


class Handler(FileSystemEventHandler):
    def on_moved(self, event: FileMovedEvent):
        if event.is_directory:
            return

        file = event.dest_path

        if not fnmatch(file, "*.json"):
            return

        with open(file, "r") as file_handle:
            json_data = json.load(file_handle)

            if "players" not in json_data:
                return

            players = json_data["players"]
            for player in players:
                world = player["world"]
                x = player["x"]
                y = player["y"]
                z = player["z"]
                player_name = player["account"]

                key = "|".join([world, str(x), str(y), str(z), player_name])

                print({
                    "key": key,
                    "timestamp": json_data["timestamp"],
                    "player": player_name,
                    "world": world,
                    "x": x,
                    "y": y,
                    "z": z
                })


observer = Observer()

observer.schedule(Handler(), os.path.join(os.environ["DYNMAP_WEB_PATH"], "standalone"))
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
