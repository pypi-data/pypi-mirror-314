"""Type stubs for poetry.poetry"""

from pathlib import Path
from typing import Any, Dict

from poetry.config.config import Config

from .packages import Package
from .repositories import Repository

class Poetry:
    """Poetry application."""
    def __init__(
        self,
        file: Path,
        local_config: Dict[str, Any],
        package: Package,
        locker: Any,
        config: Config,
        disable_cache: bool = False,
    ) -> None: ...
    @property
    def file(self) -> Path: ...
    @property
    def package(self) -> Package: ...
    @property
    def local_config(self) -> Dict[str, Any]: ...
    @property
    def locker(self) -> Any: ...
    @property
    def config(self) -> Config: ...
    @property
    def pyproject_path(self) -> Path: ...
    @property
    def pool(self) -> Repository: ...
    @property
    def disable_cache(self) -> bool: ...
