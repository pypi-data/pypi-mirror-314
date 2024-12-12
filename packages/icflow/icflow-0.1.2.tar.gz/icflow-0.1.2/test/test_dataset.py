from pathlib import Path

from iccore.runtime import ctx
from icflow.data.dataset import BaseDataset


class MockRemoteHost:

    def __init__(self) -> None:
        self.last_upload_src: Path | None = None
        self.last_upload_tgt: Path | None = None
        self.last_download_src: Path | None = None
        self.last_download_tgt: Path | None = None
        self.name = "mock_remote"

    def upload(
        self,
        source_path: Path,
        target_path: Path,
    ):
        self.last_upload_src = source_path
        self.last_upload_tgt = target_path

    def download(
        self,
        source_path: Path,
        target_path: Path,
    ):
        self.last_download_src = source_path
        self.last_download_tgt = target_path


def test_base_dataset():

    ctx.set_is_dry_run(True)

    local_dataset_path = Path("my_local_dataset")
    archive_path = Path("dataset_loc/my_dataset/my_dataset.zip")

    dataset = BaseDataset(Path("dataset_loc"), "my_dataset", hostname="localhost")
    dataset.host = MockRemoteHost()
    dataset.upload(local_dataset_path)
    assert dataset.host.last_upload_src == local_dataset_path
    assert dataset.host.last_upload_tgt == archive_path

    dataset.download(local_dataset_path)
    assert dataset.host.last_download_src == archive_path
    assert dataset.host.last_download_tgt == local_dataset_path
