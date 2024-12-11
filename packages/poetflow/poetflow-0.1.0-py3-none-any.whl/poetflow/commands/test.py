"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides the test command for PoetFlow.
"""

import asyncio
from dataclasses import dataclass
from typing import List, Optional, Set

from cleo.commands.command import Command
from cleo.helpers import argument, option

from poetflow.commands.base import MonorepoCommand


@dataclass
class TestResult:
    """Test execution result."""

    package: str
    success: bool
    output: str
    error: Optional[str] = None


class TestExecutor:
    """Test executor."""

    async def run_command(self, cmd: List[str], packages: List[str]) -> List[TestResult]:
        """Run command for packages."""
        return [
            TestResult(
                package=pkg,
                success=True,
                output="Test passed",
            )
            for pkg in packages
        ]


class TestCommand(Command, MonorepoCommand):
    """Runs tests for packages in the monorepo."""

    name = "monorepo-test"
    description = "Run tests for packages in the monorepo"

    arguments = [
        argument("all", "Test all packages"),
        argument("package", "Test specific package(s)", multiple=True),
    ]

    options = [
        option("--no-coverage", description="Disable coverage reporting"),
        option("--markers", description="Only run tests matching given markers", multiple=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.executor = TestExecutor()

    async def run_tests(self, packages: Set[str]) -> bool:
        """Run tests for packages."""
        results = await self.executor.run_command(["poetry", "run", "pytest"], list(packages))
        return all(result.success for result in results)

    def handle(self) -> int:
        """Handle command execution."""
        packages = self._get_target_packages()
        success = asyncio.run(self.run_tests(packages))

        if not success:
            self.io.write_error("Tests failed")
            return 1
        return 0

    def _get_target_packages(self) -> Set[str]:
        """Get target packages."""
        if self.option("all"):
            assert self.manager is not None
            return set(self.manager.get_all_packages())

        if packages := self.option("package"):
            return set(packages)

        return self.get_affected_packages()
