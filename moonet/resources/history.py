from __future__ import annotations

from flask import request
from flask_restful import Api, Resource

from ..services import history


class HistoryResource(Resource):
  def get(self):
    args = request.args or {}
    limit = int(args.get("limit", 50))
    page = int(args.get("page", 1))
    return {"ok": True, "items": history.list_history(limit, page)}, 200

  def delete(self):
    history.clear()
    return {"ok": True}, 200


def register(api: Api):
  api.add_resource(HistoryResource, "/history")
