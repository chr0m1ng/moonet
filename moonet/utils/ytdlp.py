from __future__ import annotations

import os
import re

import yt_dlp
from flask import current_app


def yt_thumbnail_url(video_id: str | None, quality: str = "hqdefault") -> str | None:
  return f"https://i.ytimg.com/vi/{video_id}/{quality}.jpg" if video_id else None


def extract_video_info(data: dict):
  vid = data.get("id")
  url = f"https://www.youtube.com/watch?v={vid}" if vid else None
  return {
    "title": data.get("title"),
    "url": url,
    "duration": data.get("duration"),
    "meta": {
      "thumbnail": yt_thumbnail_url(vid),
      "id": vid,
      "channel": data.get("uploader"),
      "url": url,
    }
  }


def yt_video_info(url: str):
  ydl_opts = {
    "quiet": True,
    "skip_download": True,
    "no_warrnings": True,
  }
  cookies_path = current_app.config.get("YTDLP_COOKIES_PATH")
  if cookies_path and os.path.exists(cookies_path):
    ydl_opts["cookiefile"] = cookies_path

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
    data = ydl.extract_info(url, download=False)
  return extract_video_info(dict(data))


def yt_search(query: str, limit: int | None = None, page: int = 0):
  if limit is None:
    limit = int(current_app.config.get("YTDLP_SEARCH_LIMIT", 6))

  cookies_path = current_app.config.get("YTDLP_COOKIES_PATH")
  ydl_opts = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": "in_playlist",
    "default_search": "ytsearch",
    "noplaylist": True,
  }
  if cookies_path and os.path.exists(cookies_path):
    ydl_opts["cookiefile"] = cookies_path

  # fetch enough entries for all pages up to the current one (+1 to detect has_next)
  need = page * limit + 1
  results: list[dict] = []

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
    info = ydl.extract_info(f"ytsearch{need}:{query}", download=False)
    entries = info.get("entries", []) if isinstance(info, dict) else []

    start = page * limit
    end = start + limit
    sliced = entries[start:end]
    has_next = len(entries) > end

    for e in sliced:
      results.append(extract_video_info(dict(e)))

  return {
    "page": page,
    "limit": limit,
    "has_next": has_next,
    "items": results,
  }
