from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

from .base_store import BaseStore


class VideoStore (BaseStore):
  def __init__(self, path: Path, insert_at_start: bool, max_items: int | None = None, allow_duplicates: bool = False):
    unique_keys = [] if allow_duplicates else ["id", "url"]
    super().__init__(path, insert_at_start, max_items, unique_keys)

  def add(self, entry: Dict[str, Any]):
    entry["played_at"] = int(time.time() * 1000)
    super().add(entry)
