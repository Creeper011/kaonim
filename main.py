"""Composition Root"""

import logging
import argparse
import asyncio
from src.core.constants import DEFAULT_DEBUG_FLAG
from src.infrastructure.discord.bot_factory import BotFactory
from src.infrastructure.discord.extension_loader import ExtensionLoader
from src.infrastructure.config.config_constructor import ConfigConstructor
from src.infrastructure.config.loaders.env_loader import EnvLoader
from src.infrastructure.config.loaders.toml_loader import TomlLoader

from src.infrastructure.services.random_joke_service import RandomJokeService
parser = argparse.ArgumentParser()
parser.add_argument(
    *DEFAULT_DEBUG_FLAG,
    action="store_true",
    help="Enable debug logging"
)

cli_args = parser.parse_args()

log_level = logging.INFO
if cli_args.debug:
    log_level = logging.DEBUG

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger()

discord_http_logger = logging.getLogger("discord.http")
discord_http_logger.setLevel(logging.WARNING)
discord_gateway_logger = logging.getLogger("discord.gateway")
discord_gateway_logger.setLevel(logging.WARNING)

logger.info("Logging configured with level: %s", logging.getLevelName(log_level))

config_model = ConfigConstructor({EnvLoader(logger), TomlLoader(logger)}, logger).construct()
bot = BotFactory().create_bot(token=config_model.discord.token,
                              intents=config_model.discord.intents,
                              commands_prefix=config_model.discord.prefix,
                              logger=logger)
services = {RandomJokeService()}
extension_loader = ExtensionLoader(bot=bot, services=services)
asyncio.run(extension_loader.load_extensions())
bot.run_bot(True)
