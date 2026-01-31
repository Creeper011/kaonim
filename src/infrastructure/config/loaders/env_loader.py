"""Module for loading Env configuration files."""

import logging
from pathlib import Path
from logging import Logger
from typing import Any, Optional
from dotenv import dotenv_values
from src.core.constants import DEFAULT_ENV_FILE_PATH
from src.infrastructure.config.loaders.base_loader import BaseLoader

# pylint: disable=too-few-public-methods
class EnvLoader(BaseLoader):
    """Class for loading Env configuration files."""

    def __init__(self, logger: Optional[Logger] = None,
                config_path: Path = DEFAULT_ENV_FILE_PATH) -> None:
        self.logger: Logger = logger or logging.getLogger(__name__)
        self.config_path: Path = config_path

    def load_config(self) -> dict[str, Any]:
        """Load the env configuration file.

        Returns:
            dict[str, Any]: The loaded configuration as a dictionary.
        """
        if not self.config_path.exists():
            message = f".env file not found at path: {self.config_path.resolve()}"
            self.logger.warning(message)
            raise FileNotFoundError(message)

        try:
            config = dotenv_values(dotenv_path=self.config_path)
            self.logger.debug("Env configuration loaded successfully.")
            return config
        except Exception as error:
            self.logger.exception("Failed to load env configuration: %s", error)
            raise
