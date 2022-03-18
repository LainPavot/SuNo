

import asyncio

import ticu.utils

class TiCuModule:

  name = "TiCuModule"

  def __init__(self, app, logger_name=None):
    if logger_name is None:
      logger_name = self.name
    self.logger = ticu.utils.get_logger(
      logger_name,
      filename=f"logs/{logger_name}.log",
      noprint=True
    )
    self._app = app
    self.dev = False

  def set_dev_mode(self):
    if not self.dev:
      self.dev = True
      ticu.utils.add_stdout_handler(self.logger)

  async def on_ready(self, *args, **kwargs):
    self.logger.info(f"Module {self.name} loaded and ready.")
    return False

  def __hash__(self):
    return hash(f"TiCuModule-{self.name}")