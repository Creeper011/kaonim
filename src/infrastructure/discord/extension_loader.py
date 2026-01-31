"""Module for loading extensions with DI"""

import inspect
import pkgutil
import importlib
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Iterable, Optional
from discord.ext.commands import Bot, AutoShardedBot, Cog
from src.core.constants import DEFAULT_COMMANDS_PATH

# pylint: disable=too-few-public-methods
class ExtensionLoader():
    """Class to load extensions (cogs) into the bot with dependency injection."""

    def __init__(
        self,
        bot: Bot | AutoShardedBot,
        services: Iterable[Any],
        logger: Optional[Logger] = None,
        search_path: Path = DEFAULT_COMMANDS_PATH,
    ):
        """
        Args:
            bot: The Discord Bot instance.
            search_path: The folder path (dotted string or relative path) where Cogs are located.
            services: List of service instances to be injected into Cogs.
            logger: Optional logger.
        """
        self.bot = bot
        self.search_path = search_path
        self.services = list(services)
        self.logger = logger or logging.getLogger(__name__)

    async def load_extensions(self) -> None:
        """Finds all Cogs in the search_path and loads them with dependency injection."""
        self.logger.info(
            "Starting to load extensions from '%s'...",
            self.search_path,
        )

        module_prefix = str(self.search_path).replace("/", ".").replace("\\", ".")

        loaded_count = 0
        if not self.search_path.exists():
            self.logger.error(
                "Extensions path '%s' does not exist.",
                self.search_path,
            )
            return

        for _, name, _ in pkgutil.iter_modules([str(self.search_path)]):
            full_module_name = f"{module_prefix}.{name}"

            try:
                module = importlib.import_module(full_module_name)

                for item_name in dir(module):
                    item = getattr(module, item_name)

                    if (
                        inspect.isclass(item)
                        and issubclass(item, Cog)
                        and item is not Cog
                    ):
                        await self._load_cog(item)
                        loaded_count += 1

            # pylint: disable=broad-exception-caught
            except Exception as error:
                self.logger.error(
                    "Failed to import module '%s': %s",
                    name,
                    error,
                    exc_info=True,
                )

        self.logger.info(
            "Finished loading %s extensions.",
            loaded_count,
        )

    async def _load_cog(self, cog_class: type[Cog]) -> None:
        """Instantiates a single Cog class injecting dependencies and adds to Bot."""
        try:
            cog_instance = self._inject_dependencies(cog_class)
            await self.bot.add_cog(cog_instance)
            self.logger.debug(
                "Successfully loaded Cog: %s",
                cog_class.__name__,
            )
        # pylint: disable=broad-exception-caught
        except Exception as error:
            self.logger.error(
                "Failed to load Cog '%s': %s",
                cog_class.__name__,
                error,
                exc_info=True,
            )

    def _inject_dependencies(self, cog_class: type[Cog]) -> Cog:
        """Inspects __init__, matches types with available services, and returns instance."""
        signature = inspect.signature(cog_class.__init__)
        dependencies: dict[str, Any] = {}

        for name, param in signature.parameters.items():
            if name in ("self", "bot"):
                continue

            param_type = param.annotation

            if param_type is inspect.Parameter.empty:
                self.logger.warning(
                    "Parameter '%s' in '%s' has no type hint. Skipping injection.",
                    name,
                    cog_class.__name__,
                )
                continue

            found_service = next(
                (service for service in self.services if isinstance(service, param_type)),
                None,
            )

            if found_service is None:
                if param.default is not inspect.Parameter.empty:
                    continue
                # pylint: disable=line-too-long
                raise TypeError(f"Service of type {param_type.__name__} not found for Cog {cog_class.__name__}.")

            dependencies[name] = found_service

        return cog_class(self.bot, **dependencies)
