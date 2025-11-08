from flask import current_app, request
from flask_restful import Api, Resource

from ..store import SearchHistoryStore
from ..utils.response import build_response
from ..utils.ytdlp import yt_search

search_history = SearchHistoryStore()


class Search(Resource):
  def get(self):
    query = request.args.get("query", "").strip()
    if not query:
      return build_response(False, "param query is required"), 400
    limit = request.args.get("limit", type=int)
    page = int(request.args.get("page", 0))
    if limit is None:
      limit = current_app.config.get("YTDLP_SEARCH_LIMIT", 6)
    if page == 0:
      search_history.add({"query": query})
    result = yt_search(query, limit=limit, page=page)
    return build_response(True, result), 200


class SearchHistory(Resource):
  def get(self):
    result = [item["query"] for item in search_history.list()["items"]]
    return build_response(True, result), 200

  def delete(self):
    query = request.args.get("query", "").strip()
    if not query:
      return build_response(False, "param query is required"), 400
    search_history.remove("query", query)
    return build_response(True), 200


def register(api: Api) -> None:
  api.add_resource(Search, "/search")
  api.add_resource(SearchHistory, "/search/history")
