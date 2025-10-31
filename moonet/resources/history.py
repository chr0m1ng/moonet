from __future__ import annotations

from flask import request
from flask_restful import Api, Resource

from ..services import history
from ..utils.response import build_response


class HistoryResource(Resource):
  def get(self):
    args = request.args or {}
    limit = int(args.get("limit", 50))
    page = int(args.get("page", 1))
    return build_response(True, history.list_history(limit, page)), 200

  def delete(self):
    history.clear()
    return build_response(True), 200


def register(api: Api):
  api.add_resource(HistoryResource, "/history")
