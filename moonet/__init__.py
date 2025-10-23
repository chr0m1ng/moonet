from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from flask import Flask
from flask_restful import Api

from .config import DefaultConfig
from .resources import register_resources


def create_app(config_object: str | None = None) -> Flask:
  app = Flask(__name__)

  # Logging config (optional)
  cfg_ini = Path(__file__).with_name("logging.ini")
  if cfg_ini.exists():
    logging.config.fileConfig(cfg_ini, disable_existing_loggers=False)
  app.logger.setLevel(logging.INFO)

  # Load config (defaults)
  if config_object:
    app.config.from_object(config_object)
  else:
    app.config.from_object(DefaultConfig)

  # API
  api = Api(app)

  # Modular resource registration — defer route wiring to each module
  register_resources(api)

  return app
