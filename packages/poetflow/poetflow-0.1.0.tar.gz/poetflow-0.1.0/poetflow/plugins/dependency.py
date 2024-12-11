"""Copyright (C) 2024 felipepimentel plc

This module defines classes and methods to modify the behavior of Poetry's add and remove commands
for monorepo support.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import TYPE_CHECKING

from poetry.config.config import Config
from poetry.console.commands.add import AddCommand
from poetry.console.commands.remove import RemoveCommand
from poetry.factory import Factory
from poetry.installation.installer import Installer
from poetry.poetry import Poetry
from tomlkit.toml_document import TOMLDocument

if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent
    from cleo.events.console_terminate_event import ConsoleTerminateEvent

    from poetflow.types.config import MonorangerConfig


class DummyInstaller(Installer):
    """A dummy installer that overrides the run method and disables it

    Note: For more details, refer to the docstring of `MonorepoAdderRemover`.
    """

    @classmethod
    def from_installer(cls, installer: "Installer") -> "DummyInstaller":
        """Creates a DummyInstaller instance from an existing Installer instance.

        Args:
            installer: The original installer instance.

        Returns:
            A new DummyInstaller instance with the same attributes.
        """
        new_installer = cls.__new__(cls)
        new_installer.__dict__.update(installer.__dict__)
        return new_installer

    def run(self) -> int:
        """Overrides the run method to always return 0.

        The add/remove commands will modify the pyproject.toml file only if this command returns 0.

        Returns:
            Always returns 0.
        """
        return 0


class MonorepoError(Exception):
    """Base exception for Monorepo related errors"""

    pass


class LockfileUpdateError(MonorepoError):
    """Raised when there's an error updating the lockfile"""

    pass


class MonorepoAdderRemover:
    """A class to modify the behavior of Poetry's add and remove commands for monorepo support.

    This class ensures that the add and remove commands are executed in a way that supports
    monorepo setups, including handling the shared lock file and rolling back changes if needed.
    """

    def __init__(self, plugin_conf: "MonorangerConfig") -> None:
        self.plugin_conf = plugin_conf
        self.pre_add_pyproject: None | TOMLDocument = None

    def execute(self, event: "ConsoleCommandEvent") -> None:
        """Replaces the installer with a dummy installer.

        This method creates a copy of the poetry object to prevent modification of the original
        and sets a dummy installer to disable the installation part of the add/remove commands.
        It allows modifying the pyproject.toml file without generating a per-project lockfile.

        Args:
            event: The event that triggered the command.
        """
        command = event.command
        assert isinstance(command, (AddCommand, RemoveCommand)), (
            f"{self.__class__.__name__} can only be used for `poetry add` and "
            "`poetry remove` command"
        )

        # Create a copy of the poetry object
        poetry = Poetry.__new__(Poetry)
        poetry.__dict__.update(command.poetry.__dict__)
        command.set_poetry(poetry)

        self.pre_add_pyproject = copy.deepcopy(poetry.file.read())

        installer = DummyInstaller.from_installer(command.installer)
        command.set_installer(installer)

    def post_execute(self, event: "ConsoleTerminateEvent") -> None:
        """Handles post-execution steps for add/remove commands.

        Updates the root lockfile and rolls back changes if needed.

        Args:
            event: The event that triggered the command termination.
        """
        command = event.command
        assert isinstance(command, (AddCommand, RemoveCommand)), (
            f"{self.__class__.__name__} can only be used for `poetry add` and "
            "`poetry remove` command"
        )

        io = event.io
        poetry = command.poetry

        if self.pre_add_pyproject and (poetry.file.read() == self.pre_add_pyproject):
            return

        # Force reload global config
        _ = Config.create(reload=True)
        monorepo_root: Path = (
            poetry.pyproject_path.parent / self.plugin_conf.monorepo_root
        ).resolve()
        monorepo_root_poetry = Factory().create_poetry(
            cwd=monorepo_root, io=io, disable_cache=poetry.disable_cache
        )

        installer = Installer(
            io,
            command.env,
            monorepo_root_poetry.package,
            monorepo_root_poetry.locker,
            monorepo_root_poetry.pool,
            monorepo_root_poetry.config,
            disable_cache=monorepo_root_poetry.disable_cache,
        )

        installer.dry_run(command.option("dry-run"))
        installer.verbose(io.is_verbose())
        installer.update(True)
        installer.execute_operations(not command.option("lock"))

        installer.whitelist([poetry.package.name])

        status = 0

        try:
            status = installer.run()
        except Exception as e:
            raise LockfileUpdateError(f"Failed to update lockfile: {str(e)}") from e
        finally:
            if status != 0 and not command.option("dry-run") and self.pre_add_pyproject is not None:
                io.write_line(
                    "\n<error>An error occurred during the installation. "
                    "Rolling back changes...</error>"
                )
                poetry.file.write(self.pre_add_pyproject)

            event.set_exit_code(status)
