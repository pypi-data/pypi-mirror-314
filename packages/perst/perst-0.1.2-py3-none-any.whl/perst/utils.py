import json
from pathlib import Path


def dump(data, path: str):
    with Path(path).open('w') as f:
        json.dump(data, f)


def load(path: str):
    with Path(path).open() as f:
        return json.load(f)
