from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List


class BaseStore:
  def __init__(self, path: Path, insert_at_start: bool, max_items: int | None = None):
    self.path = path
    self.insert_at_start = insert_at_start
    self.max_items = max_items

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
    vid = entry.get("id") or entry.get("url")
    items = [i for i in items if (i.get("id") or i.get("url")) != vid]
    entry["played_at"] = int(time.time() * 1000)
    if self.max_items and len(items) > self.max_items:
      items = items[:self.max_items]
    if self.insert_at_start:
      items.insert(0, entry)
    else:
      items.append(entry)
    self._save(items)

  def list(self, limit: int = 50, page: int = 1) -> dict:
    items = self._load()
    total = len(items)
    start = max((page - 1) * limit, 0)
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

  def clear(self):
    self._save([])
