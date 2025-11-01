from __future__ import annotations

from flask import request
from flask_restful import Api, Resource

from ..store import FavoritesStore
from ..utils.response import build_response
from ..utils.ytdlp import yt_video_info

store = FavoritesStore()


class FavoritesResource(Resource):

  def post(self):
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
      return build_response(False, "URL is required"), 400
    video = yt_video_info(url)
    store.add(video)
    return build_response(True), 201

  def get(self):
    args = request.args or {}
    limit = int(args.get("limit", 50))
    page = int(args.get("page", 1))
    return build_response(True, store.list(limit, page)), 200

  def delete(self):
    store.clear()
    return build_response(True), 200


def register(api: Api):
  api.add_resource(FavoritesResource, "/favorites")
