"""Path rewriter plugin."""

from typing import TYPE_CHECKING, Any, Protocol

from poetry.console.commands.command import Command

if TYPE_CHECKING:
    from poetflow.types.config import MonorangerConfig


class CommandEvent(Protocol):
    """Protocol for command events."""

    command: Any
    io: Any


class PathRewriter:
    """Rewrites paths in Poetry dependencies."""

    def __init__(self, config: "MonorangerConfig") -> None:
        self.config = config

    def execute(self, event: CommandEvent) -> None:
        """Execute the plugin."""
        if not self.config.enabled:
            return

        command = event.command
        assert isinstance(command, Command)
        # Rest of implementation...
