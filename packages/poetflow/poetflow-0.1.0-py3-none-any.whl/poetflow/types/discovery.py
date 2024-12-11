"""Package discovery functionality"""

from dataclasses import dataclass
from pathlib import Path
from typing import Set


@dataclass
class PackageInfo:
    """Information about a package"""

    name: str
    version: str
    path: Path
    dependencies: Set[str]
