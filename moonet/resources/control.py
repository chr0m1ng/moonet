import time

from flask import request
from flask_restful import Api, Resource

from ..services.mpv import MPVController
from ..utils.ytdlp import yt_search, yt_video_info

mpv = MPVController()


class Play(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url")
    query = data.get("query")
    volume = data.get("volume")
    video = {}
    if not url and not query:
      return {"error": "send url or query"}, 400
    elif query and not url:
      if not (videos := yt_search(query, limit=1)) or not (video := videos[0]):
        return {"error": "no results"}, 404
    elif url:
      video = yt_video_info(url)
    url = video.get("url")
    if not url:
      return {"error": "no valid url found"}, 404
    mpv.load(url, video.get("meta", {}))
    if volume is not None:
      mpv.set_volume(int(volume))
    deadline = time.time() + 3.0
    status = {}
    while time.time() < deadline:  # allow some time for mpv to start playback
      status = mpv.get_status()
      if status.get("playing"):
        break
    ok = status.get("playing") is True
    return {"ok": ok, "status": status}, 200


class Pause(Resource):
  def post(self):
    mpv.pause(True)
    return {"ok": True, "status": mpv.get_status()}, 200


class Resume(Resource):
  def post(self):
    mpv.pause(False)
    return {"ok": True, "status": mpv.get_status()}, 200


class Stop(Resource):
  def post(self):
    mpv.stop()
    return {"ok": True, "status": mpv.get_status()}, 200


class Volume(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    if "value" in data:
      mpv.set_volume(int(data["value"]))
    elif "delta" in data:
      mpv.add_volume(int(data["delta"]))
    else:
      return {"error": "send value (0..100) or delta"}, 400
    return {"ok": True, "status": mpv.get_status()}, 200


def register(api: Api) -> None:
  api.add_resource(Play, "/control/play")
  api.add_resource(Pause, "/control/pause")
  api.add_resource(Resume, "/control/resume")
  api.add_resource(Stop, "/control/stop")
  api.add_resource(Volume, "/control/volume")
