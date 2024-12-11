"""Copyright (C) 2024 felipepimentel plc

This module handles semantic versioning and changelog generation for packages in the monorepo.
"""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

from packaging.version import Version


class VersionBumpType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclass
class CommitInfo:
    """Information about a commit for changelog generation"""

    hash: str
    type: str
    scope: Optional[str]
    message: str
    breaking: bool


class SemanticVersionManager:
    """Manages semantic versioning for packages"""

    CONVENTIONAL_COMMIT_PATTERN = re.compile(
        r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?: (?P<message>.+)$"
    )

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def parse_commits(self, since_tag: Optional[str] = None) -> List[CommitInfo]:
        """Parses git commits to extract conventional commit information"""
        # TODO: Implement git log parsing
        return []  # Return empty list instead of None

    def determine_bump_type(self, commits: List[CommitInfo]) -> VersionBumpType:
        """Determines what type of version bump is needed based on commits

        Args:
            commits: List of commits to analyze

        Returns:
            The type of version bump needed
        """
        if any(commit.breaking for commit in commits):
            return VersionBumpType.MAJOR

        if any(commit.type in ["feat", "feature"] for commit in commits):
            return VersionBumpType.MINOR

        return VersionBumpType.PATCH

    def bump_version(self, current_version: str, bump_type: VersionBumpType) -> str:
        """Bumps a version according to semver rules

        Args:
            current_version: Current version string
            bump_type: Type of bump to perform

        Returns:
            New version string
        """
        version = Version(current_version)
        major, minor, patch = version.major, version.minor, version.micro

        if bump_type == VersionBumpType.MAJOR:
            return f"{major + 1}.0.0"
        elif bump_type == VersionBumpType.MINOR:
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
