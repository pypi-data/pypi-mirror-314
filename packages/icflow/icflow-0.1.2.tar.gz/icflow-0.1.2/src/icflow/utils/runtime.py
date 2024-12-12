"""
This module has functionality to support running in
a distributeed context
"""

import os
import socket
import logging
import json

from .devices import ComputeDevice

logger = logging.getLogger(__name__)


class NetworkContext:
    def __init__(self):
        self.hostname = ""
        self.ip_address = ""

    def read(self):
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)

    def serialize(self):
        return {"hostname": self.hostname, "ip_address": self.ip_address}

    def __str__(self):
        return json.dumps(self.serialize())


class RuntimeContext:
    """
    This holds runtime information for the session, which is mostly
    useful in a distributed setting.
    """

    def __init__(
        self,
        node_id: int = 0,
        num_nodes: int = 1,
        gpus_per_node: int = 1,
        local_rank: int = 0,
    ) -> None:

        self.local_rank = local_rank
        self.is_multigpu: bool = gpus_per_node > 1
        self.num_workers: int = 1

        self.world_size: int = gpus_per_node * num_nodes
        self.global_rank: int = node_id * gpus_per_node + local_rank

        self.device = ComputeDevice(local_rank)
        self.device.load()
        self.network_context = NetworkContext()

        self.is_initialized: bool = False

    def serialize(self):
        return {
            "local_rank": self.local_rank,
            "global_rank": self.global_rank,
            "work_size": self.world_size,
            "is_multigpu": self.is_multigpu,
            "device": self.device.serialize(),
            "num_workers": self.num_workers,
            "network": self.network_context.serialize(),
        }

    def __str__(self):
        return json.dumps(self.serialize())

    def init(self) -> None:
        """
        Should be of most interest to base classes
        """

        if self.is_initialized:
            return

        logger.info(
            "Starting runtime: world size %s, local rank %s, global rank %s",
            self.world_size,
            self.local_rank,
            self.global_rank,
        )
        self.is_initialized = True

    def is_master_process(self) -> bool:
        """
        Return true if this process has zero global rank
        """
        return self.global_rank == 0

    def sync_dict(self, input_dict: dict) -> dict:
        """
        If we are running in on multiple gpus sync dict across devices
        """
        return input_dict

    @staticmethod
    def get_slurm_info():
        return {
            "SLURM_LAUNCH_NODE_IPADDR": os.environ.get("SLURM_LAUNCH_NODE_IPADDR", ""),
            "SLURM_NPROCS": os.environ.get("SLURM_NPROCS", ""),  # world size
            "SLURM_PROCID": os.environ.get("SLURM_PROCID", ""),  # my rank
        }

    def log_cpu_info(self):
        num_cpus = os.cpu_count()
        logger.info("Num cpus: %d", num_cpus)

    def log_system_info(self):
        self.log_cpu_info()
