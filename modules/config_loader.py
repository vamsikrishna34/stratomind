import yaml
import os

CONFIG_DIR = "config"

def load_yaml_config(filename: str) -> dict:
    """
    Loads a YAML config file from the config directory.

    Args:
        filename (str): Name of the YAML file (e.g., 'model_config.yaml').

    Returns:
        dict: Parsed configuration dictionary.
    """
    path = os.path.join(CONFIG_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)