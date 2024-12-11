"""Type stubs for Poetry commands."""

from typing import Any, Callable, Protocol


class Command(Protocol):
    """Base command protocol."""

    poetry: Any
    io: Any
    env: Any
    set_poetry: Callable[[Any], None]
    set_installer: Callable[[Any], None]


class AddCommand(Command): ...


class RemoveCommand(Command): ...


class BuildCommand(Command): ...


class EnvCommand(Command): ...


class InstallCommand(Command): ...


class LockCommand(Command): ...


class UpdateCommand(Command): ...
