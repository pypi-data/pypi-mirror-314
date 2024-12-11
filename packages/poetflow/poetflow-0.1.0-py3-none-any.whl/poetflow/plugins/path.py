"""Path rewriter plugin."""

from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from poetry.console.commands.command import Command
from poetry.core.packages.directory_dependency import DirectoryDependency

if TYPE_CHECKING:
    from poetflow.types.config import MonorangerConfig


class CommandEvent(Protocol):
    """Protocol for command events."""

    command: Any
    io: Any


class PathRewriter:
    """Rewrites paths in Poetry dependencies."""

    def __init__(self, config: "MonorangerConfig") -> None:
        self.config = config

    def execute(self, event: CommandEvent) -> None:
        """Execute the plugin."""
        if not self.config.enabled:
            return

        command = event.command
        assert isinstance(command, Command)

        # Get package dependencies
        package = command.poetry.package
        if not hasattr(package, "dependency_groups"):
            return

        for group in package.dependency_groups.values():
            for dep in group.dependencies.values():
                if isinstance(dep, DirectoryDependency):
                    # Convert relative path to absolute
                    abs_path = (command.poetry.file.parent / dep.path).resolve()
                    # Convert back to relative path from monorepo root
                    monorepo_root = (
                        command.poetry.file.parent / self.config.monorepo_root
                    ).resolve()
                    try:
                        new_path = Path(abs_path).relative_to(monorepo_root)
                        dep._path = new_path
                    except ValueError:
                        # Path is not relative to monorepo root, leave it unchanged
                        pass
