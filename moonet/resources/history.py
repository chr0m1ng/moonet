from __future__ import annotations

from flask import request
from flask_restful import Api, Resource

from ..store import HistoryStore
from ..utils.response import build_response

store = HistoryStore()


class HistoryResource(Resource):
  def get(self):
    args = request.args or {}
    limit = int(args.get("limit", 50))
    page = int(args.get("page", 0))
    return build_response(True, store.list(limit, page)), 200

  def delete(self):
    store.clear()
    return build_response(True), 200


def register(api: Api):
  api.add_resource(HistoryResource, "/history")
