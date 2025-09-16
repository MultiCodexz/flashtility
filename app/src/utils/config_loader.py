# app/src/utils/config_loader.py
import json
from pathlib import Path
from app.src.utils import colored

CONFIG_DIR = Path(__file__).parent.parent / "conf"

configs = {}

def load_configs():
    for f in CONFIG_DIR.glob("*.json"):
        with open(f, "r") as file:
            data = json.load(file)
            configs[f.stem] = data
            colored.println(f"Loaded config {f.stem}: {data}")
    return configs
