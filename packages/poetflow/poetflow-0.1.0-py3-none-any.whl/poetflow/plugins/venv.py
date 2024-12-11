"""Copyright (C) 2024 felipepimentel plc

This module contains the VenvModifier class, which modifies the virtual environment (venv) for a
Poetry command. It ensures that the shared virtual environment of the monorepo root is activated
for commands that require an environment such as `poetry shell` and `poetry run`.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Protocol

from poetry.config.config import Config
from poetry.console.commands.env_command import EnvCommand
from poetry.console.commands.installer_command import InstallerCommand
from poetry.factory import Factory
from poetry.installation.installer import Installer
from poetry.utils.env import EnvManager

if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent

    from poetflow.types.config import MonorangerConfig


class CommandEvent(Protocol):
    """Protocol for command events."""

    command: Any
    io: Any


class VenvModifier:
    """A class to modify the virtual environment (venv) of poetry commands.

    This class ensures that the appropriate virtual environment is activated for commands that
    require an environment. It prevents the activation of the per-project environments and forces
    the activation of the monorepo root venv. If another venv is already activated, it does not
    activate any other venv to maintain consistency with Poetry's behavior.
    """

    def __init__(self, plugin_conf: MonorangerConfig):
        self.plugin_conf: MonorangerConfig = plugin_conf
        self.env_manager: EnvManager | None = None

    def execute(self, event: ConsoleCommandEvent) -> None:
        """Execute the plugin.

        Args:
            event: The command event
        """
        if not self.plugin_conf.enabled:
            return

        command = event.command
        if not isinstance(command, (EnvCommand, InstallerCommand)):
            return

        # Get the root poetry instance
        root_poetry = Factory.create_poetry(
            command.poetry.file.parent / self.plugin_conf.monorepo_root
        )

        # Set the root poetry instance on the command
        command.set_poetry(root_poetry)

        in_venv = bool(os.getenv("VIRTUAL_ENV"))
        if in_venv:
            return

        io = event.io

        # Force reload global config to undo changes from subproject's poetry.toml configs
        _ = Config.create(reload=True)
        monorepo_root = (
            root_poetry.pyproject_path.parent / self.plugin_conf.monorepo_root
        ).resolve()
        monorepo_root_poetry = Factory().create_poetry(
            cwd=monorepo_root, io=io, disable_cache=root_poetry.disable_cache
        )

        io.write_line(f"<info>Using monorepo root venv <fg=green>{monorepo_root.name}</></info>\n")
        env_manager = EnvManager(monorepo_root_poetry, io=io)
        root_env = env_manager.create_venv()

        command.set_env(root_env)

        if not isinstance(command, InstallerCommand):
            return

        # Update installer for commands that require an installer
        installer = Installer(
            io,
            root_env,
            command.poetry.package,
            command.poetry.locker,
            command.poetry.pool,
            command.poetry.config,
            disable_cache=command.poetry.disable_cache,
        )
        command.set_installer(installer)
