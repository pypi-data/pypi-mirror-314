"""Configuration types for PoetFlow."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MonorangerConfig:
    """Configuration for the Monoranger plugin."""

    enabled: bool
    monorepo_root: Path
    packages_dir: Optional[str] = None
    version_rewrite_rule: Optional[str] = None
