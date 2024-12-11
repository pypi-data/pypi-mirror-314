"""Changelog generation functionality."""

from pathlib import Path
from typing import List, Optional

from ..types.versioning import CommitInfo


class ChangelogGenerator:
    """Generates changelog from commits."""

    def __init__(self, project_root: Path):
        """Initialize changelog generator.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root

    def generate_markdown(self, version: str, commits: List[CommitInfo]) -> str:
        """Generates a markdown changelog entry for a version.

        Args:
            version: Version number
            commits: List of commits to include

        Returns:
            Markdown formatted changelog
        """
        lines = [f"## {version}", ""]

        # Group commits by type
        breaking_changes = [c for c in commits if c.breaking]
        features = [c for c in commits if c.type in ["feat", "feature"]]
        fixes = [c for c in commits if c.type == "fix"]

        # Add breaking changes
        if breaking_changes:
            lines.extend(["### Breaking Changes", ""])
            for commit in breaking_changes:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        # Add features
        if features:
            lines.extend(["### Features", ""])
            for commit in features:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        # Add fixes
        if fixes:
            lines.extend(["### Bug Fixes", ""])
            for commit in fixes:
                scope = f"**{commit.scope}:** " if commit.scope else ""
                lines.append(f"- {scope}{commit.message}")
            lines.append("")

        return "\n".join(lines)

    def write_changelog(
        self,
        version: str,
        commits: List[CommitInfo],
        output_file: Optional[Path] = None,
    ) -> None:
        """Write changelog to a file."""
        content = self.generate_markdown(version, commits)
        changelog_path = output_file or (self.project_root / "CHANGELOG.md")

        # Prepend new content to existing changelog
        if changelog_path.exists():
            existing_content = changelog_path.read_text()
            content = f"{content}\n{existing_content}"

        changelog_path.write_text(content)
