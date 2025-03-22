from datetime import datetime

import yaml
from easydict import EasyDict as edict


def datetime_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> datetime:
    return datetime.strptime(node.value, "%H:%M")


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!time", datetime_constructor)
    return loader


def get_configs(file="configs"):
    # configs ou credentials
    with open(f"core/{file}.yaml") as file:
        data = yaml.load(file, Loader=get_loader())
        return edict(data)
