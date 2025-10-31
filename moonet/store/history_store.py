from __future__ import annotations

from ..config import DefaultConfig
from .base_store import BaseStore


class HistoryStore(BaseStore):
  def __init__(self):
    super().__init__(DefaultConfig.HISTORY_PATH, insert_at_start=True, max_items=DefaultConfig.HISTORY_MAX)
