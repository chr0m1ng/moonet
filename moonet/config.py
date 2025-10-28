from pathlib import Path

# root directory of the project (same as this file)
ROOT_DIR = Path(__file__).resolve().parent

# data directory
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class DefaultConfig:
  DEBUG = False
  TESTING = False
  HOST = "0.0.0.0"
  PORT = 8080
  MPV_SOCKET = "/tmp/moonet-mpv.sock"
  DEFAULT_VOLUME = 60
  YTDLP_SEARCH_LIMIT = 6
  YTDLP_COOKIES_PATH = None
  DEFAULT_BT_MAC = "C0:28:8D:10:6A:ED"
  HISTORY_PATH = DATA_DIR / "history.json"
  HISTORY_MAX = 100
