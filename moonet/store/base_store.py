from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List


class BaseStore:
  def __init__(self, path: Path, insert_at_start: bool, max_items: int | None = None, unique_keys: List[str] = []):
    self.path = path
    self.insert_at_start = insert_at_start
    self.max_items = max_items
    self.unique_keys = unique_keys

  def _ensure_file(self):
    self.path.parent.mkdir(parents=True, exist_ok=True)
    if not self.path.exists():
      self.path.write_text("[]", encoding="utf-8")

  def _load(self) -> List[Dict[str, Any]]:
    self._ensure_file()
    try:
      return json.loads(self.path.read_text(encoding="utf-8"))
    except Exception:
      return []

  def _save(self, items: List[Dict[str, Any]]):
    self.path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")

  def add(self, entry: Dict[str, Any]):
    items = self._load()
    unique_values = {key: entry.get(key) for key in self.unique_keys if key in entry}
    if unique_values:
      items = [i for i in items if not any(i.get(k) == v for k, v in unique_values.items())]
    if self.max_items and len(items) > self.max_items:
      items = items[:self.max_items]
    if self.insert_at_start:
      items.insert(0, entry)
    else:
      items.append(entry)
    self._save(items)

  def list(self, limit: int = 50, page: int = 0) -> dict:
    items = self._load()
    total = len(items)
    start = page * limit
    end = start + limit
    sliced = items[start:end]
    has_next = end < total
    return {
      "page": page,
      "limit": limit,
      "total": total,
      "has_next": has_next,
      "items": sliced,
    }

  def remove(self, key: str, value: str):
    items = self._load()
    items = [i for i in items if i.get(key) != value]
    self._save(items)

  def clear(self):
    self._save([])
