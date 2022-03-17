

import asyncio
import atexit
import os

import discord

import ticu.utils


logger = ticu.utils.get_logger(__name__, filename=f"{__name__}.log", noprint=True)


class App(discord.Client):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def stop(self):
    logger.info("TiCu is shutting down.")

  async def on_ready(self):
    logger.info(f"Logged in as {self.user.name} - {self.user.id}")
    logger.info("------")

  def run(self, dev=False):
    if dev:
      ticu.utils.add_stdout_handler(logger)
    super().run(self.token)
