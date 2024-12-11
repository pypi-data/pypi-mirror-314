"""Types for versioning and changelog functionality."""

import re
from dataclasses import dataclass
from typing import Optional

from ..core.exceptions import PackageError


@dataclass
class Version:
    """Represents a semantic version."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """Parse version string into Version object."""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str)
        if not match:
            raise PackageError(f"Invalid version format: {version_str}")
        return cls(major=int(match.group(1)), minor=int(match.group(2)), patch=int(match.group(3)))

    def __str__(self) -> str:
        """Convert version to string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump(self, bump_type: str) -> "Version":
        """Create new version with bumped number."""
        if bump_type == "major":
            return Version(self.major + 1, 0, 0)
        elif bump_type == "minor":
            return Version(self.major, self.minor + 1, 0)
        elif bump_type == "patch":
            return Version(self.major, self.minor, self.patch + 1)
        else:
            raise PackageError(f"Invalid bump type: {bump_type}")


@dataclass
class CommitInfo:
    """Information about a commit."""

    type: str
    scope: Optional[str]
    message: str
    breaking: bool = False

    @classmethod
    def parse(cls, commit_message: str) -> "CommitInfo":
        """Parse a conventional commit message.

        Format: type(scope): message
        Example: feat(core): add new feature

        Args:
            commit_message: The commit message to parse

        Returns:
            CommitInfo instance
        """
        # Check for breaking change marker
        breaking = "!" in commit_message
        commit_message = commit_message.replace("!", "")

        # Parse conventional commit format
        pattern = r"^(\w+)(?:\(([^)]+)\))?: (.+)$"
        match = re.match(pattern, commit_message)

        if not match:
            return cls(type="other", scope=None, message=commit_message, breaking=breaking)

        return cls(
            type=match.group(1), scope=match.group(2), message=match.group(3), breaking=breaking
        )
