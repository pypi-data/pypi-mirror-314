"""LockModifier plugin for Poetry."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from poetry.config.config import Config
from poetry.console.commands.install import InstallCommand
from poetry.console.commands.lock import LockCommand
from poetry.console.commands.update import UpdateCommand
from poetry.factory import Factory
from poetry.installation.installer import Installer

if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent

    from poetflow.types.config import MonorangerConfig
    from tests.types import MockEvent

    EventType = Union[ConsoleCommandEvent, MockEvent]


class LockModifier:
    """Modifies Poetry's lock command behavior."""

    def __init__(self, config: MonorangerConfig) -> None:
        self.plugin_conf = config

    def execute(self, event: "EventType") -> None:
        """Execute the plugin.

        Args:
            event: Command event
        """
        if not self.plugin_conf.enabled:
            return

        command = event.command
        assert isinstance(command, (LockCommand, InstallCommand, UpdateCommand)), (
            f"{self.__class__.__name__} can only be used for "
            "`poetry lock`, `poetry install`, and `poetry update` commands"
        )

        io = event.io
        io.write_line("<info>Running command from monorepo root directory</info>")

        # Force reload global config
        _ = Config.create(reload=True)
        monorepo_root = (
            command.poetry.pyproject_path.parent / self.plugin_conf.monorepo_root
        ).resolve()
        monorepo_root_poetry = Factory().create_poetry(
            cwd=monorepo_root, io=io, disable_cache=command.poetry.disable_cache
        )

        command.set_poetry(monorepo_root_poetry)

        installer = Installer(
            io,
            command.env,
            monorepo_root_poetry.package,
            monorepo_root_poetry.locker,
            monorepo_root_poetry.pool,
            monorepo_root_poetry.config,
            disable_cache=monorepo_root_poetry.disable_cache,
        )
        command.set_installer(installer)
