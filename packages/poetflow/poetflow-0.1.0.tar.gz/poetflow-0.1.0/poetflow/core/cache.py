"""Cache management for PoetFlow"""

from pathlib import Path
from typing import Optional


class CacheManager:
    def __init__(self, cache_dir: Optional[Path]):
        self.cache_dir = cache_dir
