"""Base class for configuration loaders."""

from abc import abstractmethod
from typing import Any

# pylint: disable=too-few-public-methods
# pylint: disable=unnecessary-ellipsis

class BaseLoader():
    """Base class for configuration loaders."""
    @abstractmethod
    def load_config(self) -> dict[str, Any]:
        """Load the configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        ...
