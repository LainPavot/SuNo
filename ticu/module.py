

import asyncio

import ticu.utils


logger = ticu.utils.get_logger(__name__, filename=f"{__name__}.log", noprint=True)


class TiCuModule:

  name = "TiCuModule"

  def __init__(self, app):
    self._app = app
    self.dev = False

  def set_dev_mode(self):
    if not self.dev:
      self.dev = True
      ticu.utils.add_stdout_handler(logger)

  async def on_ready(self, *args, **kwargs):
    logger.info(f"Module {self.name} loaded and ready.")
    return False

