import json


def get_config():
    with open("config.json", "r") as fp:
        config = json.load(fp)
        return config
