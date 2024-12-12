"""
This module is for workflow sessions
"""

import os
import json
from pathlib import Path
import logging

from iccore import time_utils

from icflow.utils.runtime import RuntimeContext
from icflow.session import SessionSettings


logger = logging.getLogger(__name__)


class WorkflowSession:
    """
    A workflow session is an instance of a workflow being
    executed, possibly in parallel over multiple workers.
    """

    def __init__(
        self,
        result_dir: Path = Path(),
        runtime_context: RuntimeContext = RuntimeContext(),
    ) -> None:

        self.runtime_ctx = runtime_context
        self.result_dir = result_dir

        self.tasks: list = []
        self.tasks_initialized = False

    @staticmethod
    def setup_result_dir(result_dir: Path):
        """
        Utility to create a result directory with a timestamp
        -based name.
        """
        current_time = time_utils.get_timestamp_for_paths()
        result_dir = result_dir / Path(current_time)
        os.makedirs(result_dir, exist_ok=True)
        return result_dir

    def save_config(self, settings: SessionSettings):
        """
        Save the config used to define the workflow
        """
        config_output_path = self.result_dir / "initial_config.json"
        output_content = settings.serialize()
        with open(config_output_path, "w", encoding="utf-8") as f:
            json.dump(output_content, f)

    def init_tasks(self):
        """
        Perform any step needed to initialize tasks
        """
        self.tasks_initialized = True

    def run_tasks(self):
        """
        Run any available tasks
        """

        if not self.tasks_initialized:
            self.init_tasks()

        if not self.tasks:
            logger.info("No tasks available to launch")
            return

        logger.info("Launching %d tasks", len(self.tasks))

        for idx, task in enumerate(self.tasks):
            logger.info("Launching %d of %d tasks: %s", idx, len(self.tasks), task.name)
            task.launch()

        logger.info("Finished launching tasks")
