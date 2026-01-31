"""Factory module for creating Discord bot instances."""

from logging import Logger
from discord import Intents
from src.infrastructure.discord.basebot import BaseBot

class BotFactory():
    """BotFactory is responsible for creating and configuring Discord bot instances."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    def create_bot(token: str, commands_prefix: str, intents: Intents, logger: Logger) -> BaseBot:
        """Creates and returns a configured BaseBot instance.

        Args:
            commands_prefix (str): The command prefix for the bot.
            logger (Logger): Logger instance for logging.
        Returns:
            BaseBot: Configured Discord bot instance.
        """
        bot = BaseBot(token=token, commands_prefix=commands_prefix, intents=intents, logger=logger)
        return bot
