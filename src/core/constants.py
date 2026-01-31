"""Module-level constants for the project."""

from pathlib import Path

DEFAULT_TOML_CONFIG_PATH: Path = Path("config.toml")
DEFAULT_ENV_FILE_PATH: Path = Path(".env")
DEFAULT_COMMAND_PREFIX: str = "!"
DEFAULT_DEBUG_FLAG = ("-d", "--debug")
DEFAULT_COMMANDS_PATH = Path("src/interface/cogs")
