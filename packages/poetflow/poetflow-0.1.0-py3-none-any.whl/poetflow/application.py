"""Application module."""

from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.application import Application as PoetryApplication

from poetflow.core.monorepo import MonoRepo


class Application(PoetryApplication):
    """Application class."""

    def __init__(self, monorepo: MonoRepo) -> None:
        super().__init__()
        self.monorepo = monorepo

    def handle_command_event(self, event: ConsoleCommandEvent) -> None:
        """Handle command event."""
        # Instead of calling execute_command directly
        command = event.command
        if hasattr(command, "set_manager"):
            command.set_manager(self.monorepo)
