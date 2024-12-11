"""Custom type definitions for TOML handling"""

from typing import Any, Dict, Protocol, TypeVar


class TOMLDocument(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


TOMLData = Dict[str, Any]
T = TypeVar("T")
