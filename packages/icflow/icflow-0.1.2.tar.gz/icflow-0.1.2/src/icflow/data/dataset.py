"""
This module has functionaly for handling datasets that feed into
models.
"""

from pathlib import Path
import logging

from iccore import filesystem as fs
from icsystemutils.network.remote import RemoteHost

logger = logging.getLogger(__name__)


class BaseDataset:
    """
    This class represents a collection of model input data.
    The data can be remote - in which case instances can be
    used to sync with it
    """

    def __init__(
        self, path: Path, name: str = "", archive_name: str = "", hostname: str = ""
    ) -> None:
        self.name = name
        self.archive_name = archive_name if archive_name else self.name + ".zip"
        self.host: RemoteHost | None = None
        if hostname:
            self.host = RemoteHost(hostname)
        self.path = path

    def archive(self, dst: Path):
        """
        Archive the dataset in the provided location
        """
        archive_name, archive_format = self.archive_name.split(".")
        fs.make_archive(Path(archive_name), archive_format, dst)

    def upload(self, loc: Path):
        """
        Upload the dataset to the given path
        """
        archive_path = self._get_archive_path()
        if loc.is_dir():
            logger.info("Zipping dataset %s", self.archive_name)
            self.archive(loc)
            logger.info("Finished zipping dataset %s", self.archive_name)
            loc = loc / self.archive_name
        if self.host:
            logger.info(
                "Uploading %s to remote at %s:%s", loc, self.host.name, archive_path
            )
            self.host.upload(loc, archive_path)
            logger.info("Finished Uploading %s to %s", loc, archive_path)
        else:
            logger.info("Doing local copy of %s to %s", loc, archive_path)
            fs.copy(loc, archive_path)
            logger.info("Finished local copy of %s to %s", loc, archive_path)

    def download(self, loc: Path):
        """
        Download the dataset from the given path
        """
        archive_path = self._get_archive_path()
        if self.host:
            remote = f"{self.host.name}:{archive_path}"
            logger.info("Downloading remote %s to %s", remote, loc)
            self.host.download(archive_path, loc)
        else:
            logger.info("Copying %s to %s", archive_path, loc)
            fs.copy(archive_path, loc)

        archive_loc = loc / self.archive_name
        logger.info("Unpacking %s to %s", archive_path, loc)
        fs.unpack_archive(archive_loc, loc)

    def _get_archive_path(self) -> Path:
        return self.path / Path(self.name) / Path(self.archive_name)
