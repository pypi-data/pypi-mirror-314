"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides configuration management for PoetFlow.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class Config:
    """Configuration for PoetFlow."""

    root_dir: Path
    packages_dir: Path
    enabled: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create config from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            Config instance
        """
        root_dir = Path(data.get("root_dir", "."))
        packages_dir = root_dir / data.get("packages_dir", "packages")
        enabled = data.get("enabled", True)
        log_level = data.get("log_level", "INFO")

        return cls(
            root_dir=root_dir, packages_dir=packages_dir, enabled=enabled, log_level=log_level
        )

    def __init__(
        self,
        root_dir: Optional[Path] = None,
        packages_dir: Optional[Path] = None,
        enabled: bool = True,
        log_level: str = "INFO",
    ):
        """Initialize configuration.

        Args:
            root_dir: Root directory path
            packages_dir: Packages directory path
            enabled: Whether PoetFlow is enabled
            log_level: Logging level
        """
        self.root_dir = root_dir or Path(".")
        self.packages_dir = packages_dir or self.root_dir / "packages"
        self.enabled = enabled
        self.log_level = log_level
