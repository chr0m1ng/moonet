from __future__ import annotations

import json
import time
from typing import Any, Dict, List

from ..config import DefaultConfig

HISTORY_PATH = DefaultConfig.HISTORY_PATH
HISTORY_MAX = DefaultConfig.HISTORY_MAX


def _ensure_file():
  HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
  if not HISTORY_PATH.exists():
    HISTORY_PATH.write_text("[]", encoding="utf-8")


def _load() -> List[Dict[str, Any]]:
  _ensure_file()
  try:
    return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
  except Exception:
    return []


def _save(items: List[Dict[str, Any]]):
  HISTORY_PATH.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def add(entry: Dict[str, Any]):
  items = _load()
  vid = entry.get("id") or entry.get("url")
  items = [i for i in items if (i.get("id") or i.get("url")) != vid]
  entry["played_at"] = int(time.time() * 1000)
  items.insert(0, entry)
  if len(items) > HISTORY_MAX:
    items = items[:HISTORY_MAX]
  _save(items)


def list_history(limit: int = 50, page: int = 1) -> dict:
  items = _load()
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


def clear():
  _save([])
