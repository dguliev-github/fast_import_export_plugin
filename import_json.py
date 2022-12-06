import json
import os
import pathlib

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("settings.json") as settings_file:
    settings = json.load(settings_file)
