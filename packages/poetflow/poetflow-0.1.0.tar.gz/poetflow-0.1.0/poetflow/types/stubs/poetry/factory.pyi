"""Type stubs for poetry.factory"""

from pathlib import Path
from typing import Any, Optional

class Factory:
    @classmethod
    def create_poetry(
        cls, cwd: Path, io: Optional[Any] = None, disable_cache: bool = False
    ) -> Any: ...
