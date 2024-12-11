"""Hook system for PoetFlow"""

from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar("T")


class HookManager:
    """Manages hooks for PoetFlow"""

    _hooks: Dict[str, List[Callable[..., Any]]] = {}

    @classmethod
    def register(cls, hook_name: str, callback: Callable[..., Any]) -> None:
        """Register a hook callback

        Args:
            hook_name: Name of the hook
            callback: Function to be called when hook is triggered
        """
        if hook_name not in cls._hooks:
            cls._hooks[hook_name] = []
        cls._hooks[hook_name].append(callback)
