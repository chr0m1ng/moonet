from flask import request
from flask_restful import Api, Resource

from moonet.services.bluetooth import bt_reconnect


class BluetoothConnect(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    mac = data.get("mac")
    ok = bt_reconnect(mac)
    return {"ok": ok, "mac": mac}, (200 if ok else 500)


def register(api: Api) -> None:
  api.add_resource(BluetoothConnect, "/bluetooth/connect")
