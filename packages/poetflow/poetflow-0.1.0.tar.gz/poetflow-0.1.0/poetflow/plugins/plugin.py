"""Base plugin class."""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class CommandEvent(Protocol):
    """Protocol for command events."""

    command: Any
    io: Any


class Plugin(ABC):
    """Base class for all plugins."""

    @abstractmethod
    def execute(self, event: CommandEvent) -> None:
        """Execute the plugin.

        Args:
            event: The command event
        """
        pass
