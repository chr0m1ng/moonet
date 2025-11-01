from __future__ import annotations

import json
import os
import socket
import subprocess
import threading
import time
from typing import overload

from flask import current_app


class MPVController:
  def __init__(self):
    self._proc: subprocess.Popen | None = None
    self._lock = threading.Lock()

  @property
  def sock(self) -> str:
    return current_app.config["MPV_SOCKET"]

  def _socket_ok(self) -> bool:
    try:
      with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(0.5)
        s.connect(self.sock)
        ping = {"command": ["get_property", "idle-active"]}
        s.sendall((json.dumps(ping) + "\n").encode())
        _ = s.recv(4096)
        return True
    except Exception:
      return False

  @overload
  def _send(self, payload: dict) -> dict: ...
  @overload
  def _send(self, payload: list) -> list: ...

  def _send(self, payload) -> dict | list:
    self._ensure_running()

    if isinstance(payload, list):
      data = "".join(json.dumps(cmd) + "\n" for cmd in payload).encode()
    else:
      data = (json.dumps(payload) + "\n").encode()

    with socket.socket(socket.AF_UNIX) as s:
      s.connect(self.sock)
      s.sendall(data)
      s.shutdown(socket.SHUT_WR)

      resp = b""
      while True:
        chunk = s.recv(4096)
        if not chunk:
          break
        resp += chunk

    lines = [l for l in resp.decode(errors="ignore").splitlines() if l.strip()]
    results = [json.loads(l) for l in lines if l.startswith("{")]

    if isinstance(payload, list):
      return results
    return results[0] if results else {"error": "empty response"}

  def _ensure_running(self):
    with self._lock:
      if self._proc and self._proc.poll() is None and os.path.exists(self.sock) and self._socket_ok():
        return

      if (not self._proc) and os.path.exists(self.sock) and self._socket_ok():
        return

      try:
        if os.path.exists(self.sock) and not self._socket_ok():
          os.remove(self.sock)
      except FileNotFoundError:
        pass

      if not os.path.exists(self.sock):
        cmd = [
          "mpv",
          "--no-video",
          "--idle=yes",
          "--force-window=no",
          f"--input-ipc-server={self.sock}",
          "--audio-display=no",
          f"--volume={current_app.config['DEFAULT_VOLUME']}",
          "--ytdl=yes",
        ]
        ytdl_raw_opts = ["extractor-args=youtube:player_client=android"]
        cookies_path = current_app.config.get("YTDLP_COOKIES_PATH")
        if cookies_path:
          ytdl_raw_opts.insert(0, f"cookies={cookies_path}")
        cmd.append("--ytdl-raw-options=" + ",".join(ytdl_raw_opts))

        self._proc = subprocess.Popen(
          cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        deadline = time.time() + 5
        while time.time() < deadline:
          if os.path.exists(self.sock) and self._socket_ok():
            return
          time.sleep(0.05)
        raise RuntimeError("mpv did not initialize IPC socket in time")

  def load(self, url: str, meta: dict | None = None) -> dict:
    self.pause(False)
    self.set_video_meta(meta)
    return self._send({"command": ["loadfile", url, "replace"]})

  def set_video_meta(self, data: dict | None):
    self._send({"command": ["set_property", "user-data/meta", json.dumps(data)]})

  def get_video_meta(self) -> dict | None:
    resp = self._send({"command": ["get_property", "user-data/meta"]})
    data = resp.get("data")
    if data:
      try:
        return json.loads(data)
      except Exception:
        return None
    return None

  def pause(self, state: bool) -> dict:
    return self._send({"command": ["set_property", "pause", state]})

  def stop(self) -> dict:
    self.set_video_meta(None)
    return self._send({"command": ["stop"]})

  def set_volume(self, value: int) -> dict:
    v = max(0, min(100, int(value)))
    return self._send({"command": ["set_property", "volume", v]})

  def add_volume(self, delta: int) -> dict:
    return self._send({"command": ["add", "volume", int(delta)]})

  def get_status(self) -> dict:
    props = ["pause", "volume", "time-pos", "duration", "media-title"]
    cmds = [{"command": ["get_property", p]} for p in props]

    results = self._send(cmds)
    out = {p: r.get("data") for p, r in zip(props, results)}

    out["playing"] = out.get("pause") is False and out.get("time-pos") is not None
    out["meta"] = self.get_video_meta()

    for key, value in out.items():
      out[key.replace("-", "_")] = value
    return out
