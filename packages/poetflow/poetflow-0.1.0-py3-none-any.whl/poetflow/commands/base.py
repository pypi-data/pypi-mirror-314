"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides the base command class for PoetFlow.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Set

from poetflow.types import Command as PoetryCommand

if TYPE_CHECKING:
    from poetflow.types import MonorepoManager


class MonorepoCommand(PoetryCommand, ABC):
    """Base class for all monorepo commands"""

    def __init__(self) -> None:
        super().__init__()
        self.manager: Optional["MonorepoManager"] = None

    def set_manager(self, manager: "MonorepoManager") -> None:
        """Set monorepo manager

        Args:
            manager: The monorepo manager
        """
        self.manager = manager

    @abstractmethod
    def handle(self) -> int:
        """Handle command execution

        Returns:
            Exit code
        """
        pass

    def get_affected_packages(self) -> Set[str]:
        """Get packages affected by changes

        Returns:
            Set of package names

        Raises:
            AssertionError: If manager is not set
        """
        assert self.manager is not None, "Manager must be set before calling get_affected_packages"
        return self.manager.get_affected_packages()
