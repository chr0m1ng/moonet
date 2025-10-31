from flask_restful import Api, Resource

from ..utils.response import build_response


class Health(Resource):
  def get(self):
    return build_response(True), 200


def register(api: Api) -> None:
  api.add_resource(Health, "/health")
