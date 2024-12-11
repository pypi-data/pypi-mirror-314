"""Type stubs for poetry.console.commands.build"""

from poetry.console.commands.command import Command

class BuildCommand(Command):
    """Build command protocol."""
    def handle(self) -> int: ...
