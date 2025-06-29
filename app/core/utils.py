import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.resolve()

def get_model_path(model_name: str) -> Path:
    return get_project_root() / "app" / "models" / model_name

def log(message: str):
    print(f"[ResQNet] {message}")