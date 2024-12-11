"""Type stubs for poetry.console.commands.add"""

from typing import List, Optional

from poetry.console.commands.installer_command import InstallerCommand

class AddCommand(InstallerCommand):
    """Add command stub."""
    def __init__(self) -> None: ...
    def handle(self) -> int: ...
    def add_dependencies(
        self,
        packages: List[str],
        allow_prereleases: Optional[bool] = None,
    ) -> None: ...
