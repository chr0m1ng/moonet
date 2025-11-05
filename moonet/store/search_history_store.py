from __future__ import annotations

from ..config import DefaultConfig
from .base_store import BaseStore


class SearchHistoryStore(BaseStore):
  def __init__(self):
    super().__init__(DefaultConfig.SEARCH_HISTORY_PATH, insert_at_start=True, max_items=DefaultConfig.SEARCH_HISTORY_MAX)
