"""Copyright (C) 2024 felipepimentel plc

This module handles semantic versioning and changelog generation for packages in the monorepo.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Union

from tomlkit.container import Container
from tomlkit.items import Item, Table

from poetflow.core.exceptions import PackageError
from poetflow.types.monorepo import MonoRepo
from poetflow.types.tomlkit import dumps, parse, table
from poetflow.types.versioning import CommitInfo

TOMLValue = Union[str, int, float, bool, Dict[str, Any], List[Any], Item, Container]
TOMLMapping = Dict[str, TOMLValue]

T = TypeVar("T")


class ChangelogGenerator:
    """Generates changelogs from commit information"""

    def generate_markdown(self, version: str, commits: List[CommitInfo]) -> str:
        """Generate markdown changelog

        Args:
            version: Version number
            commits: List of commits

        Returns:
            Markdown formatted changelog
        """
        lines = [
            f"## {version}",
            "",
            f"*Released on {datetime.now().strftime('%Y-%m-%d')}*",
            "",
        ]

        # Add breaking changes
        breaking = [c for c in commits if c.breaking]
        if breaking:
            lines.extend(["### Breaking Changes", ""])
            for commit in breaking:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        # Add features
        features = [c for c in commits if c.type == "feat" and not c.breaking]
        if features:
            lines.extend(["### Features", ""])
            for commit in features:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        # Add fixes
        fixes = [c for c in commits if c.type == "fix" and not c.breaking]
        if fixes:
            lines.extend(["### Bug Fixes", ""])
            for commit in fixes:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        return "\n".join(lines)


class VersionManager:
    """Manages versioning for packages"""

    def __init__(self, monorepo: MonoRepo) -> None:
        """Initialize version manager

        Args:
            monorepo: MonoRepo instance
        """
        self.monorepo = monorepo

    def _bump_major(self, version: str) -> str:
        major, _, _ = version.split(".")
        return f"{int(major) + 1}.0.0"

    def _bump_minor(self, version: str) -> str:
        major, minor, _ = version.split(".")
        return f"{major}.{int(minor) + 1}.0"

    def _bump_patch(self, version: str) -> str:
        major, minor, patch = version.split(".")
        return f"{major}.{minor}.{int(patch) + 1}"

    def get_next_version(self, package: str, commits: List[CommitInfo]) -> str:
        """Get next version based on conventional commits

        Args:
            package: Package name
            commits: List of commits

        Returns:
            Next version number

        Raises:
            PackageError: If package not found
        """
        pkg_info = self.monorepo.get_package_info(package)
        if not pkg_info:
            raise PackageError(f"Package {package} not found")

        current = str(pkg_info["version"])
        breaking_changes = [c for c in commits if c.breaking]
        features = [c for c in commits if c.type == "feat"]
        fixes = [c for c in commits if c.type == "fix"]

        if breaking_changes:
            return self._bump_major(current)
        elif features:
            return self._bump_minor(current)
        elif fixes:
            return self._bump_patch(current)

        return current

    def update_version(self, package: str, version: str) -> None:
        """Update package version

        Args:
            package: Package name
            version: New version

        Raises:
            PackageError: If package not found or if TOML structure is invalid
        """
        pkg_info = self.monorepo.get_package_info(package)
        if not pkg_info:
            raise PackageError(f"Package {package} not found")

        pkg_path = Path(str(pkg_info["path"]))
        pyproject_path = pkg_path / "pyproject.toml"

        with open(pyproject_path) as f:
            pyproject = parse(f.read())

        # Create tool.poetry section if it doesn't exist
        if "tool" not in pyproject:
            tool_table = table()
            pyproject.add("tool", tool_table)

        tool_section: Optional[Table] = pyproject.get("tool")  # type: ignore
        if not isinstance(tool_section, Table):
            raise PackageError("Invalid pyproject.toml: 'tool' section is missing or invalid")

        if "poetry" not in tool_section:
            poetry_table = table()
            tool_section.add("poetry", poetry_table)

        poetry_section: Optional[Table] = tool_section.get("poetry")  # type: ignore
        if not isinstance(poetry_section, Table):
            raise PackageError(
                "Invalid pyproject.toml: 'tool.poetry' section is missing or invalid"
            )

        poetry_section["version"] = version

        with open(pyproject_path, "w") as f:
            f.write(dumps(pyproject))
