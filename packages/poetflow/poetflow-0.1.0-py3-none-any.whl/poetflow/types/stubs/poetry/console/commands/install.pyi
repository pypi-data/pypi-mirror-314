"""Type stubs for poetry.console.commands.install"""

from poetry.console.commands.command import Command

class InstallCommand(Command):
    """Install command protocol."""
    def handle(self) -> int: ...
