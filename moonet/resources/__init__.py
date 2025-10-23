from flask_restful import Api

from . import bluetooth, control, health, search, status


def register_resources(api: Api) -> None:
  health.register(api)
  status.register(api)
  control.register(api)
  search.register(api)
  bluetooth.register(api)
