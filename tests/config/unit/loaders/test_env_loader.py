"""Unit tests for the EnvLoader class."""

from unittest.mock import MagicMock, patch
from pathlib import Path
from src.infrastructure.config.loaders.env_loader import EnvLoader

def test_env_loader_load_success() -> None:
    """Test loading an env configuration file successfully."""
    logger_mock = MagicMock()

    fake_path = MagicMock(spec=Path)
    fake_path.exists.return_value = True
    fake_path.resolve.return_value = "/fake/.env"
    fake_path.name = ".env"

    with patch("src.infrastructure.config.loaders.env_loader.dotenv_values",
               return_value={"key1": "value1", "key2": "value2"}):

        env_loader = EnvLoader(logger=logger_mock, config_path=fake_path)
        data = env_loader.load_config()

    assert data == {"key1": "value1", "key2": "value2"}
    fake_path.exists.assert_called_once()

def test_env_loader_with_invalid_path() -> None:
    """Test loading an env configuration file from an invalid path."""
    logger_mock = MagicMock()

    fake_path = MagicMock(spec=Path)
    fake_path.exists.return_value = False
    fake_path.resolve.return_value = "/invalid/path/.env"

    env_loader = EnvLoader(logger=logger_mock, config_path=fake_path)

    try:
        env_loader.load_config()
    # pylint: disable=broad-exception-caught
    except Exception as error:
        assert str(error) == f".env file not found at path: {fake_path.resolve()}"
        logger_mock.warning.assert_called()

def test_env_loader_with_empty_env() -> None:
    """Test loading an empty .env configuration file."""
    logger_mock = MagicMock()

    fake_path = MagicMock(spec=Path)
    fake_path.exists.return_value = True

    with patch("src.infrastructure.config.loaders.env_loader.dotenv_values", return_value={}):

        env_loader = EnvLoader(logger=logger_mock, config_path=fake_path)
        data = env_loader.load_config()

    assert data == {}

def test_env_with_malformed_env() -> None:
    """Test loading a malformed .env configuration file."""
    logger_mock = MagicMock()

    fake_path = MagicMock(spec=Path)
    fake_path.exists.return_value = True

    with patch("src.infrastructure.config.loaders.env_loader.dotenv_values",
               side_effect=Exception("Malformed .env")):

        env_loader = EnvLoader(logger=logger_mock, config_path=fake_path)

        try:
            env_loader.load_config()
        # pylint: disable=broad-exception-caught
        except Exception as error:
            assert str(error) == "Malformed .env"
            logger_mock.exception.assert_called()
