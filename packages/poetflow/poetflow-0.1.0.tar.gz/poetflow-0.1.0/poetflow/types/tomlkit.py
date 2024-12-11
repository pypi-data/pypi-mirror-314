"""Tomlkit types and utilities."""

from typing import Any, Callable, Dict, Mapping, Union

import tomlkit
from tomlkit.container import Container
from tomlkit.items import Item, Table
from tomlkit.toml_document import TOMLDocument

# Re-export for convenience
parse = tomlkit.parse
table = tomlkit.table

# Define type for dumps function with explicit sort_keys parameter
DumpsFunction = Callable[[Union[TOMLDocument, Mapping[str, Any]], bool], str]
dumps = tomlkit.dumps  # type: ignore

TOMLValue = Union[str, int, float, bool, Dict[str, Any], list[Any], Item, Container]
TOMLMapping = Dict[str, TOMLValue]

__all__ = ["parse", "table", "dumps", "TOMLValue", "TOMLMapping", "Table"]
