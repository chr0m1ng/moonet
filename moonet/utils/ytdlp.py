from __future__ import annotations

import os

import yt_dlp
from flask import current_app

YT_DLP_OPTS = {
  "quiet": True,
  "skip_download": True,
  "extract_flat": "in_playlist",
  "default_search": "ytsearch",
  "noplaylist": True,
  "no_check_certificate": True
}


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
  cookies_path = current_app.config.get("YTDLP_COOKIES_PATH")
  if cookies_path and os.path.exists(cookies_path):
    YT_DLP_OPTS["cookiefile"] = cookies_path

  with yt_dlp.YoutubeDL(YT_DLP_OPTS) as ydl:  # type: ignore
    data = ydl.extract_info(url, download=False)
  return extract_video_info(dict(data))


def yt_search(query: str, limit: int | None = None, page: int = 0):
  if limit is None:
    limit = int(current_app.config.get("YTDLP_SEARCH_LIMIT", 6))

  cookies_path = current_app.config.get("YTDLP_COOKIES_PATH")
  if cookies_path and os.path.exists(cookies_path):
    YT_DLP_OPTS["cookiefile"] = cookies_path

  # fetch enough entries for all pages up to the current one (+1 to detect has_next)
  need = (page + 1) * limit + 1
  results: list[dict] = []

  with yt_dlp.YoutubeDL(YT_DLP_OPTS) as ydl:  # type: ignore
    info = ydl.extract_info(f"ytsearch{need}:{query}", download=False)
    entries = info.get("entries", []) if isinstance(info, dict) else []

    start = page * limit
    end = start + limit
    sliced = entries[start:end]

    for e in sliced:
      results.append(extract_video_info(dict(e)))

  return {
    "page": page,
    "limit": limit,
    "has_next": True,
    "items": results,
  }
