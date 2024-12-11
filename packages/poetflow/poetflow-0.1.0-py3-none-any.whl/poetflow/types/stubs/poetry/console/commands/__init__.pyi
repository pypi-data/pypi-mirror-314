"""Type stubs for poetry.console.commands"""

from abc import ABCMeta
from typing import Any

from cleo.io.io import IO
from poetry.poetry import Poetry
from poetry.utils.env import Env

class Command(metaclass=ABCMeta):
    """Base command protocol."""
    @property
    def poetry(self) -> Poetry: ...
    @property
    def io(self) -> IO: ...
    @property
    def env(self) -> Env: ...
    def option(self, name: str, help: str = "", is_array: bool = False, **kwargs: Any) -> Any: ...
    def set_poetry(self, poetry: Poetry) -> None: ...
    def set_installer(self, installer: Any) -> None: ...
    def set_env(self, env: Env) -> None: ...
    def set_manager(self, manager: Any) -> None: ...

class AddCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class BuildCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class EnvCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class InstallCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class LockCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class RemoveCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class UpdateCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

class SelfCommand(Command):
    env: Env
    io: IO
    poetry: Poetry

__all__ = [
    "Command",
    "AddCommand",
    "BuildCommand",
    "EnvCommand",
    "InstallCommand",
    "LockCommand",
    "RemoveCommand",
    "UpdateCommand",
    "SelfCommand",
]
