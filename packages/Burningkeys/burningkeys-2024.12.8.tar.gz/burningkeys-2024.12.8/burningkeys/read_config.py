import json
import os
import sys
from functools import cache
from pathlib import Path

file_name = "burningkeys.json"


def _read_config():
    path = Path(os.curdir) / file_name

    if not path.exists():
        print(f"No {file_name} file found at {Path(os.curdir).resolve()}", file=sys.stderr)
        sys.exit(-1)

    with open(path) as file:
        _config = json.load(file)
    return _config


@cache
def config():
    return _read_config()
