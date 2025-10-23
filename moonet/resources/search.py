from flask import current_app, request
from flask_restful import Api, Resource

from ..utils.ytdlp import yt_search


class Search(Resource):
  def get(self):
    q = request.args.get("q", "").strip()
    if not q:
      return {"error": "param q is required"}, 400
    limit = request.args.get("limit", type=int)
    if limit is None:
      limit = current_app.config.get("YTDLP_SEARCH_LIMIT", 6)
    items = yt_search(q, limit=limit)
    return {"items": items, "limit": limit}, 200


def register(api: Api) -> None:
  api.add_resource(Search, "/search")
