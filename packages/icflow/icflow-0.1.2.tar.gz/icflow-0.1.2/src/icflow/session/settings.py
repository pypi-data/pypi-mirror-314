import json

from icflow.utils.serialization import Config


class SessionSettings:
    def __init__(self, file=None) -> None:
        self.data = Config()
        self.model = Config()
        self.runtime = Config()

        if file is not None:
            self.load_from_file(file)

    def update_model_setting(self, key, value):
        self.model[key] = value

    def update_data_setting(self, key, value):
        self.data[key] = value

    def load_from_file(self, file):
        with open(file, "r") as f:
            self.deserialize(json.load(f))

    def deserialize(self, content):
        if "data" in content:
            self.data = Config(content["data"])

        if "model" in content:
            self.model = Config(content["model"])

        if "runtime" in content:
            self.runtime = Config(content["runtime"])

    def serialize(self):
        return {
            "data": self.data.data,
            "model": self.model.data,
            "runtime": self.runtime.data,
        }

    def __str__(self) -> str:
        return str(self.serialize())
