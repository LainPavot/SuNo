

import asyncio
import atexit
import os

import discord

import ticu.utils

logger = ticu.utils.get_logger(__name__, filename=f"{__name__}.log", noprint=True)

class App(discord.Client):

  def __init__(self, *args, **kwargs):
    self._pidfile = None
    super().__init__(*args, **kwargs)

  @property
  def pidfile(self):
    return self._pidfile

  @pidfile.setter
  def pidfile(self, pidfile):
    if self._pidfile is not None:
        os.unlink(self.pidfile)
    self._pidfile = pidfile
    if self.pidfile is not None:
        if os.path.exists(self.pidfile):
            with open(self.pidfile, "r") as pid:
                pid = pid.read()
            raise RuntimeError(f"This bot is already running - pid: {pid}.")
        with open(self.pidfile, "w") as pid:
          pid.write(f"{os.getpid()}")

  def stop(self):
    logger.info("TiCu is shutting down.")
    if self.pidfile is not None:
      os.unlink(self.pidfile)

  async def on_ready(self):
    logger.info(f"Logged in as {self.user.name} - {self.user.id}")
    logger.info("------")

  def run(self, dev=False):
    atexit.register(self.stop)
    if dev:
        ticu.utils.add_stdout_handler(logger)
    super().run(self.token)
