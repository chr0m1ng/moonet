from flask_restful import Api, Resource

from ..services.mpv import MPVController
from ..utils.response import build_response

mpv = MPVController()


class Status(Resource):
  def get(self):
    try:
      return build_response(True, mpv.get_status()), 200
    except Exception as e:
      return build_response(False, str(e)), 500


def register(api: Api) -> None:
  api.add_resource(Status, "/status")
