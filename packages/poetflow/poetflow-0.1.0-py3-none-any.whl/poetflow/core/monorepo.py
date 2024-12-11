"""Monorepo management."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from poetflow.core.config import Config
from poetflow.core.dependencies import DependencyManager
from poetflow.core.versioning import VersionManager
from poetflow.types.discovery import PackageInfo
from poetflow.types.monorepo import MonoRepo as MonoRepoProtocol


class MonoRepo(MonoRepoProtocol):
    """Manages a monorepo."""

    def __init__(self, config: Config) -> None:
        """Initialize monorepo."""
        self.root_path: Path = config.root_dir
        self.config: Config = config
        self.version_manager: VersionManager = VersionManager(self)
        self.dependency_manager: DependencyManager = DependencyManager(self)
        self._packages: Dict[str, PackageInfo] = {}
        self._load_packages()

    def _load_packages(self) -> None:
        """Load packages from disk."""
        # Implementation here
        pass

    @property
    def root(self) -> str:
        """Get root directory."""
        return str(self.root_path)

    @property
    def packages(self) -> List[str]:
        """Get list of packages."""
        return list(self._packages.keys())

    def get_all_packages(self) -> List[str]:
        """Get all packages."""
        return self.packages

    def get_package_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get package information."""
        pkg = self._packages.get(name)
        if not pkg:
            return None
        return {
            "name": pkg.name,
            "version": pkg.version,
            "path": str(pkg.path),
            "dependencies": list(pkg.dependencies),
        }
