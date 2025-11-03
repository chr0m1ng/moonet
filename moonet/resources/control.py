import time

from flask import request
from flask_restful import Api, Resource

from ..services.mpv import MPVController
from ..store import HistoryStore
from ..utils.response import build_response
from ..utils.ytdlp import yt_search, yt_video_info

mpv = MPVController()
history = HistoryStore()


class Play(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url")
    query = data.get("query")
    volume = data.get("volume")
    video = {}
    if not url and not query:
      return build_response(False, "send url or query"), 400
    elif query and not url:
      if not (videos := yt_search(query, limit=1).get("items")) or not (video := videos[0]):
        return build_response(False, "no results"), 404
    elif url:
      video = yt_video_info(url)
    url = video.get("url")
    if not url:
      return build_response(False, "no valid url found"), 404
    mpv.load(url, video.get("meta", {}))
    if volume is not None:
      mpv.set_volume(int(volume))
    status = mpv.get_status_when("playing", True)
    ok = status.get("playing") is True
    if video:
      history.add(video)
    return build_response(ok, status if ok else "Could not play video"), 200


class Pause(Resource):
  def post(self):
    mpv.pause(True)
    status = mpv.get_status_when("pause", True)
    return build_response(True, status), 200


class Resume(Resource):
  def post(self):
    mpv.pause(False)
    status = mpv.get_status_when("playing", True)
    return build_response(True, status), 200


class Stop(Resource):
  def post(self):
    mpv.stop()
    status = mpv.get_status_when("idle-active", True)
    return build_response(True, status), 200


class Volume(Resource):
  def post(self):
    data = request.get_json(force=True, silent=True) or {}
    if "value" in data:
      mpv.set_volume(int(data["value"]))
    elif "delta" in data:
      mpv.add_volume(int(data["delta"]))
    else:
      return build_response(False, "send value (0..100) or delta"), 400
    return build_response(True, mpv.get_status()), 200


def register(api: Api) -> None:
  api.add_resource(Play, "/control/play")
  api.add_resource(Pause, "/control/pause")
  api.add_resource(Resume, "/control/resume")
  api.add_resource(Stop, "/control/stop")
  api.add_resource(Volume, "/control/volume")
