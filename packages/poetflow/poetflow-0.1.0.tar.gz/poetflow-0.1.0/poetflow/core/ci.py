"""CI utilities."""

from typing import Set

from poetflow.types.monorepo import MonoRepo


class CIManager:
    """Manages CI operations."""

    def __init__(self, monorepo: MonoRepo) -> None:
        self.monorepo = monorepo

    def get_affected_packages(self) -> Set[str]:
        """Get affected packages."""
        affected: Set[str] = set()
        for package in self.monorepo.packages:  # Use packages property
            affected.add(package)
        return affected

    def get_dependent_packages(self) -> Set[str]:
        """Get dependent packages."""
        dependent: Set[str] = set()
        for package in self.monorepo.packages:  # Use packages property
            dependent.add(package)
        return dependent
