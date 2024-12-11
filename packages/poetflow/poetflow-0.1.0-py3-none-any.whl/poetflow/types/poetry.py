"""Type definitions for Poetry classes."""

from pathlib import Path
from typing import Protocol

from cleo.io.io import IO


class Command(Protocol):
    """Base command protocol."""

    @property
    def poetry(self) -> "Poetry": ...

    @property
    def io(self) -> IO: ...


class Poetry(Protocol):
    """Poetry application protocol."""

    @property
    def pyproject_path(self) -> Path: ...

    @property
    def disable_cache(self) -> bool: ...


__all__ = ["Command", "Poetry"]
