"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides plugin registration and management.
"""

from typing import Dict, Type

from poetflow.plugins.base import Plugin
from poetflow.types.exceptions import PluginError


class PluginRegistry:
    """Registry for PoetFlow plugins"""

    _plugins: Dict[str, Type[Plugin]] = {}

    @classmethod
    def register(cls, name: str, plugin_class: Type[Plugin]) -> None:
        """Register a plugin

        Args:
            name: Plugin name
            plugin_class: Plugin class

        Raises:
            PluginError: If plugin is already registered
        """
        if name in cls._plugins:
            raise PluginError(f"Plugin {name} already registered")

        cls._plugins[name] = plugin_class

    @classmethod
    def get_plugin(cls, name: str) -> Type[Plugin]:
        """Get a plugin by name

        Args:
            name: Plugin name

        Returns:
            Plugin class

        Raises:
            PluginError: If plugin not found
        """
        try:
            return cls._plugins[name]
        except KeyError as err:
            raise PluginError(f"Plugin {name} not found") from err
