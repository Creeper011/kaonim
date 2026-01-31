"""Module for loading TOML configuration files."""

import logging
from pathlib import Path
from tomllib import load
from logging import Logger
from typing import Any, Optional
from src.core.constants import DEFAULT_TOML_CONFIG_PATH
from src.infrastructure.config.loaders.base_loader import BaseLoader

# pylint: disable=too-few-public-methods
class TomlLoader(BaseLoader):
    """Class for loading TOML configuration files."""

    def __init__(self, logger: Optional[Logger] = None,
                config_path: Path = DEFAULT_TOML_CONFIG_PATH) -> None:
        self.logger: Logger = logger or logging.getLogger(__name__)
        self.config_path: Path = config_path

    def load_config(self) -> dict[str, Any]:
        """Load the TOML configuration file.

        Returns:
            dict[str, Any]: The loaded configuration as a dictionary.
        """
        self.logger.debug("Loading TOML configuration from %s", self.config_path)
        try:
            with self.config_path.open("rb") as toml_file:
                config = load(toml_file)
                self.logger.debug("TOML configuration loaded successfully.")
                return config
        except Exception as error:
            self.logger.error("Failed to load TOML configuration: %s", error)
            raise
