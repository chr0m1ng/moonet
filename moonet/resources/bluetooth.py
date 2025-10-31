from flask import request
from flask_restful import Api, Resource

from ..services.bluetooth import bt_reconnect
from ..utils.response import build_response


class BluetoothConnect(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    mac = data.get("mac")
    ok = bt_reconnect(mac)
    return build_response(ok, mac), (200 if ok else 500)


def register(api: Api) -> None:
  api.add_resource(BluetoothConnect, "/bluetooth/connect")
