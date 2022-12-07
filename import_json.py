import json
import os
import pathlib

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("settings.json") as settings_file:
    settings = json.load(settings_file)

def show_arguments(**kwargs):
    for arg in kwargs:
        print(arg)
"""
test

def predefined_keys(first, second, third):
    print(f"first = {first}, second = {second}, third = {third}")

predefined_dict = {"first" : "alpha", "second" : "bravo", "third" : "charlie"}
"""