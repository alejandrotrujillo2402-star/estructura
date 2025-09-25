import json
import os

def load_config(path="config.json"):
    # Ajusta la ruta al directorio de main.py
    base_dir = os.path.dirname(__file__)  
    full_path = os.path.join(base_dir, "..", path)
    with open(full_path, "r") as f:
        return json.load(f)
