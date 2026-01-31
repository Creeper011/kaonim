"""Test configuration loading integration."""

from unittest.mock import MagicMock, patch
from pathlib import Path
from src.infrastructure.config.loaders.env_loader import EnvLoader
from src.infrastructure.config.loaders.toml_loader import TomlLoader
from src.infrastructure.config.config_constructor import ConfigConstructor

def test_full_config_loading_integration() -> None:
    """Test full configuration loading integration."""
    logger_mock = MagicMock()

    fake_env_path = MagicMock(spec=Path)
    fake_env_path.exists.return_value = True
    fake_env_path.resolve.return_value = "/fake/.env"
    fake_env_path.name = ".env"

    fake_toml_path = MagicMock(spec=Path)
    fake_toml_path.open.return_value.__enter__.return_value.read.return_value = b"""
    [discord]
    prefix = ";?"

    [discord.intents]
    guilds = true
    messages = true
    message_content = true
    """

    with patch("src.infrastructure.config.loaders.env_loader.dotenv_values",
            return_value={"TOKEN": "special token", "not_in_mapping_value": "value"}), \
        patch("src.infrastructure.config.loaders.toml_loader.Path.open",
              return_value=fake_toml_path.open.return_value):
        env_loader = EnvLoader(logger=logger_mock, config_path=fake_env_path)
        toml_loader = TomlLoader(logger=logger_mock, config_path=fake_toml_path)

        config_constructor = ConfigConstructor(loaders={env_loader, toml_loader},
                                            logger=logger_mock)
        config_model = config_constructor.construct()

    assert config_model.discord.prefix == ";?"
    assert config_model.discord.intents is not None
    assert config_model.discord.intents.guilds is True
    assert config_model.discord.intents.messages is True
    assert config_model.discord.intents.message_content is True
    assert config_model.discord.token == "special token"
    assert hasattr(config_model, "not_in_mapping_value") is False
