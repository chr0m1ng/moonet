from flask import current_app, request
from flask_restful import Api, Resource

from ..utils.response import build_response
from ..utils.ytdlp import yt_search


class Search(Resource):
  def get(self):
    q = request.args.get("q", "").strip()
    if not q:
      return {"error": "param q is required"}, 400
    limit = request.args.get("limit", type=int)
    page = int(request.args.get("page", 1))
    if limit is None:
      limit = current_app.config.get("YTDLP_SEARCH_LIMIT", 6)
    result = yt_search(q, limit=limit, page=page)
    return build_response(True, result), 200


def register(api: Api) -> None:
  api.add_resource(Search, "/search")
