from __future__ import annotations

from ..config import DefaultConfig
from .base_store import BaseStore


class FavoriteStore(BaseStore):
  def __init__(self):
    super().__init__(DefaultConfig.FAVORITE_PATH, insert_at_start=True)
