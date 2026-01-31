""""Configuration constructor module."""

import logging
from typing import Any, Set
from logging import Logger
from discord import Intents
from src.infrastructure.config.config_model import ConfigModel, DiscordConfiguration
from src.infrastructure.config.loaders.base_loader import BaseLoader
from src.core.constants import DEFAULT_COMMAND_PREFIX

# pylint: disable=too-few-public-methods
class ConfigConstructor():
    """Construct config model from loaded configuration data."""

    def __init__(self, loaders: Set[BaseLoader], logger: Logger) -> None:
        self.loaders: Set[BaseLoader] = loaders
        self.logger: Logger = logger or logging.getLogger(__name__)

    def _load_configuration(self) -> dict[str, Any]:
        """Load configuration data from all loaders."""
        config = {}
        for loader in self.loaders:
            config.update(loader.load_config())
        return config

    def _parser_values(self, raw_config: dict[str, Any]) -> dict[str, Any]:
        """Parse raw configuration values to appropriate types."""

        if "discord" in raw_config and "intents" in raw_config["discord"]:
            intents_config = raw_config["discord"]["intents"]
            parsed_intents = self._parse_intents(intents_config)
            raw_config["discord"]["intents"] = parsed_intents

        return raw_config

    def _parse_intents(self, intents_config: dict[str, bool]) -> Intents:
        """Parse all discord intents"""

        intents = Intents.none()
        for intent_name, enabled in intents_config.items():
            if not isinstance(enabled, bool) or not enabled:
                continue

            try:
                setattr(intents, intent_name, True)
                self.logger.debug(f"Activated intent: {intent_name}")
            except AttributeError:
                self.logger.warning(f"'{intent_name}' is not a valid intent. ignoring it")

        return intents

    def _map_config(self, raw_config: dict[str, Any]) -> ConfigModel:
        """Map parsed configuration dictionary to ConfigModel structure."""
        return ConfigModel(discord=DiscordConfiguration(
            token=raw_config.get("TOKEN", ""),
            intents=raw_config.get("discord", {}).get("intents", Intents.default()),
            prefix=raw_config.get("discord", {}).get("prefix", DEFAULT_COMMAND_PREFIX)
        ))

    def construct(self) -> ConfigModel:
        """Construct the configuration model from loaded data."""
        raw_config = self._load_configuration()
        parsed_config = self._parser_values(raw_config)
        config_model = self._map_config(parsed_config)
        return config_model
