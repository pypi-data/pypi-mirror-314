"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides the base plugin class for PoetFlow.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from cleo.events.console_terminate_event import ConsoleTerminateEvent

if TYPE_CHECKING:
    from poetflow.types.config import MonorangerConfig
    from tests.types import MockEvent


class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, config: "MonorangerConfig") -> None:
        """Initialize plugin.

        Args:
            config: Plugin configuration
        """
        self.config = config

    @abstractmethod
    def execute(self, event: "MockEvent") -> None:
        """Execute the plugin

        Args:
            event: Command event
        """
        pass

    @abstractmethod
    def post_execute(self, event: ConsoleTerminateEvent) -> None:
        """Execute after command completion

        Args:
            event: The terminate event
        """
        pass
