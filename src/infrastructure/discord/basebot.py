"""Base bot class for the Discord bot implementation."""

import logging
from logging import Logger
from discord.ext.commands import AutoShardedBot
from discord import Intents

class BaseBot(AutoShardedBot):
    """A base class for the Discord bot, extending AutoShardedBot."""

    def __init__(self, token: str, commands_prefix: str, intents: Intents,
                 logger: Logger, **kwargs) -> None:
        super().__init__(command_prefix=commands_prefix, intents=intents, **kwargs)
        self.token = token
        self.logger: Logger = logger or logging.getLogger(__name__)

    async def on_ready(self) -> None:
        """Event handler called when the bot is ready."""
        self.logger.info(f"Bot is ready. Logged in as {self.user}")
        await self.tree.sync()

    def run_bot(self, reconnect: bool = True) -> None:
        """Runs the bot"""
        return super().run(self.token, reconnect=reconnect)
