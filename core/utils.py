from datetime import datetime
from pathlib import Path

import yaml
from easydict import EasyDict as edict


def datetime_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> datetime:
    return datetime.strptime(node.value, "%H:%M")


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!time", datetime_constructor)
    return loader


def _read_file(file):
    f = Path(file)
    for _ in range(5):
        if f.exists():
            break
        f = ".." / f
    else:
        raise FileNotFoundError(f"File not found: {file}")

    with open(file) as file:
        data = yaml.load(file, Loader=get_loader())
        return edict(data)


def get_configs():
    return _read_file(f"configs/configs.yaml")


def get_provider(provider):
    return _read_file(f"configs/providers/{provider}.yaml")
