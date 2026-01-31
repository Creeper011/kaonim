"""Data models for configuration settings."""

from dataclasses import dataclass
from discord import Intents

@dataclass(frozen=True)
class DiscordConfiguration():
    """Data model for Discord configuration settings."""
    token: str
    intents: Intents
    prefix: str

@dataclass(frozen=True)
class ConfigModel():
    """Data model for configuration settings."""
    discord: DiscordConfiguration
