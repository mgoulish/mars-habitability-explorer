import json


def read_config(filename):
    """Read in the config file and return a config dictionary"""
    with open(filename) as f:
        data = json.loads(f.read())

        return data
