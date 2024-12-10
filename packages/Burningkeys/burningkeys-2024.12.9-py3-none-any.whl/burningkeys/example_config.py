import json
import os
import sys
from pathlib import Path

import burningkeys.read_config as config


def create():
    path = Path(os.curdir) / config.file_name

    if path.exists():
        print(f"{config.file_name} file already exists at {Path(os.curdir).resolve()}")
        sys.exit(-1)

    path.touch(exist_ok=False)

    with open(path, "w") as file:
        json.dump({
            "Ctrl+p": ["echo Hi, printing something or something"],
            "Ctrl+Alt+m": [
                "echo This is the first command",
                "echo And this is the second"
            ]
        }, file, indent="\t")
