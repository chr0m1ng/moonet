from flask_restful import Api, Resource


class Health(Resource):
  def get(self):
    return {"status": "ok"}


def register(api: Api) -> None:
  api.add_resource(Health, "/health")
