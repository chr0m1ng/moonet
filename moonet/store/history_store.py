from __future__ import annotations

from ..config import DefaultConfig
from .video_store import VideoStore


class HistoryStore(VideoStore):
  def __init__(self):
    super().__init__(DefaultConfig.HISTORY_PATH, insert_at_start=True, max_items=DefaultConfig.HISTORY_MAX, allow_duplicates=True)
