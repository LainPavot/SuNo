

import asyncio
import atexit
import os

import discord

import ticu.utils


logger = ticu.utils.get_logger(__name__, filename=f"logs/{__name__}.log", noprint=True)


class App(discord.Client):

  def __init__(self, *args, **kwargs):
    self._modules = []
    super().__init__(*args, **kwargs)

  def register(self, module):
    """
    Registers a TiCu Module
    Module must inherit from TiCuModule
    """
    if module not in self._modules:
      self._modules.append(module)

  def stop(self):
    logger.info("TiCu is shutting down.")

  async def on_ready(self, *args, **kwargs):
    logger.info(f"Logged in as {self.user.name} - {self.user.id}")
    logger.info("------")
    await self.map_modules("on_ready", args, kwargs)

  async def map_modules(self, func_name, args=(), kwargs={}):
    """
    Take a function's name and parameter and call each module's function
    with the given name.
    The functions must return True if the dispatching must stop.
    False otherwise
    """
    for module in self._modules:
      dispatcher = getattr(module, func_name)
      result = await dispatcher(*args, **kwargs)
      if result:
        break
      if result is None:
        ValueError(
          f"The module {module.name} did not dispatch correctly "
          f"for the function {func_name}. Expected True or False, got None."
        )

  def run(self, dev=False):
    if dev:
      ticu.utils.add_stdout_handler(logger)
      for module in self._modules:
        module.set_dev_mode()
    super().run(self.token)
