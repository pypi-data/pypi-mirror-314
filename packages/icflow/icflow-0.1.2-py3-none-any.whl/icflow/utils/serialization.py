from pathlib import Path
import yaml


class Config:
    """
    Small wrapper over a dict with convenience methods like loading keys
    with default values
    """

    def __init__(self, data: dict = {}) -> None:
        self.data = data
        self.path: None | Path = None

    @staticmethod
    def _get(dict: dict, key: str, default=None):
        if key in dict:
            return dict[key]
        else:
            return default

    def get(self, key: str, default=None):
        return Config._get(self.data, key, default)

    def get_child(self, key: str, subkey: str, default=None):
        parent = Config._get(self.data, key)
        if parent is not None:
            return Config._get(parent, subkey, default)

    def load(self, path: Path):
        self.path = path
        with open(path, "r") as f:
            self.data = yaml.safe_load(f)
