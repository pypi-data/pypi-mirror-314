"""Type stubs for poetry.console.commands.env_command"""

from poetry.console.commands.command import Command

class EnvCommand(Command):
    """Environment command protocol."""
    def handle(self) -> int: ...
