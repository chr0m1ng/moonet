from __future__ import annotations

from ..config import DefaultConfig
from .video_store import VideoStore


class FavoriteStore(VideoStore):
  def __init__(self):
    super().__init__(DefaultConfig.FAVORITE_PATH, insert_at_start=True)
