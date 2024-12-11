"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides parallel execution capabilities for running commands across multiple packages.
"""

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from poetflow.monorepo import MonorepoManager


@dataclass
class CommandResult:
    """Result of executing a command"""

    package: str
    success: bool
    output: str
    error: Optional[str] = None


class ParallelExecutor:
    """Executes commands across multiple packages in parallel"""

    def __init__(self, manager: MonorepoManager, max_workers: int = 4):
        self.manager = manager
        self.max_workers = max_workers

    async def run_command(
        self, command: List[str], packages: Optional[List[str]] = None, cwd: Optional[Path] = None
    ) -> List[CommandResult]:
        """Runs a command across multiple packages

        Args:
            command: Command to run as list of strings
            packages: List of package names to run command for. If None, runs for all packages.
            cwd: Working directory for command execution. If None, uses package directory.

        Returns:
            List of CommandResult objects
        """
        if packages is None:
            packages = self.manager.get_build_order()

        semaphore = asyncio.Semaphore(self.max_workers)
        tasks: List[asyncio.Task[CommandResult]] = []

        async def run_single(package: str) -> CommandResult:
            async with semaphore:
                pkg = self.manager.get_package(package)
                pkg_dir = cwd or pkg.info.path

                try:
                    proc = await asyncio.create_subprocess_exec(
                        *command,
                        cwd=pkg_dir,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )

                    stdout, stderr = await proc.communicate()
                    success = proc.returncode == 0

                    return CommandResult(
                        package=package,
                        success=success,
                        output=stdout.decode(),
                        error=stderr.decode() if stderr else None,
                    )
                except Exception as e:
                    return CommandResult(package=package, success=False, output="", error=str(e))

        for pkg in packages:
            task = asyncio.create_task(run_single(pkg))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return list(results)
