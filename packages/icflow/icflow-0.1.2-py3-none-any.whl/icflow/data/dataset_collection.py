from pathlib import Path
import os
import argparse
import logging

from iccore.runtime import ctx

from icflow.data.dataset import BaseDataset
from icflow.utils.serialization import Config


class DatasetCollection:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.datasets: dict = {}
        self.load()

    def upload_item(self, name: str, location: Path):
        if name in self.datasets:
            self.datasets[name].upload(location)
        else:
            raise RuntimeError(f"Requested dataset {name} not found.")

    def download_item(self, name, location: Path):
        if name in self.datasets:
            self.datasets[name].download(location)
        else:
            raise RuntimeError(f"Requested dataset {name} not found.")

    def load(self):
        for config_entry in self.config.data:
            name = config_entry["name"]
            self.datasets[name] = BaseDataset(Config(config_entry))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--location", type=Path)
    parser.add_argument("--dry_run", type=bool, default=False)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    ctx.set_is_dry_run(args.dry_run)

    dataset_config = Config()
    dataset_config.load(Path(args.config))

    datasets = DatasetCollection(dataset_config)
    datasets.load()

    location = Path(args.location)
    if not location.is_absolute():
        location = Path(os.getcwd()) / location

    if args.action == "upload":
        datasets.upload_item(args.dataset, location)
    elif args.action == "download":
        datasets.download_item(args.dataset, location)
