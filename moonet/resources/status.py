from flask_restful import Api, Resource

from ..services.mpv import MPVController

mpv = MPVController()


class Status(Resource):
  def get(self):
    try:
      return mpv.get_status(), 200
    except Exception as e:
      return {"error": str(e)}, 500


def register(api: Api) -> None:
  api.add_resource(Status, "/status")
