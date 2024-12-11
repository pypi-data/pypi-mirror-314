"""Venv modifier plugin for Poetry."""

from typing import Any, Protocol

from poetry.utils.env import EnvManager

from poetflow.types.config import MonorangerConfig


class CommandEvent(Protocol):
    """Protocol for command events."""

    command: Any
    io: Any


class VenvModifier:
    """Modifies Poetry's virtual environment behavior."""

    def __init__(self, config: MonorangerConfig) -> None:
        self.config = config
        self.env_manager: EnvManager | None = None

    def execute(self, event: CommandEvent) -> None:
        """Execute the plugin.

        Args:
            event: The command event
        """
        if not self.config.enabled:
            return
