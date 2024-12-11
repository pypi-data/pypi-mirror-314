"""Type definitions for Poetry application."""

from typing import Any, Callable, Protocol


class EventDispatcher(Protocol):
    """Protocol for event dispatcher."""

    def add_listener(self, event_name: str, listener: Callable[..., Any]) -> None: ...


class Application(Protocol):
    """Protocol for Poetry application."""

    event_dispatcher: EventDispatcher
