

import asyncio
import logging
import os

import discord

import suno.config
import suno.database
import suno.sync
import suno.utils


logger = suno.utils.get_logger(__name__, filename=f"logs/{__name__}.log", noprint=True)


class App(discord.Client):

  def __init__(self, *args, **kwargs):
    self._modules = []
    self.config = suno.config
    self.dev = False
    self.sync_manager = suno.sync.SyncManager
    self.sync_manager.conf = self.config
    self.role_sync = suno.sync.RoleSync()
    for action in self.role_sync.syncable_role_action:
      action = f"{self.role_sync.prefix}{action}"
      setattr(self, action, getattr(self.role_sync, action))
    super().__init__(*args, **kwargs)

  def register(self, module):
    """
    Registers a SuNo Module
    Module must inherit from SuNoModule
    """
    if module not in self._modules:
      self._modules.append(module)

  def stop(self):
    logger.info("SuNo is shutting down.")

  async def on_ready(self, *args, **kwargs):
    logger.info(f"Logged in as {self.user.name} - {self.user.id}")
    logger.info("------")
    await self.map_modules("on_ready", args, kwargs)

  async def on_message(self, message, *args, **kwargs):
    if message.author.bot:
      return
    args = (message, *args)
    if message.content == self.config.LOAD_COMMAND:
      return await self.load_everythin(message)
    await self.map_modules("on_message", args, kwargs)

  async def on_guild_available(self, guild):
    await self.load_everythin(None, guild)

  async def on_member_join(self, *args, **kwargs):
    await self.map_modules("on_member_join", args, kwargs)

  async def on_reaction_add(self, *args, **kwargs):
    await self.map_modules("on_reaction_add", args, kwargs)

  async def on_reaction_remove(self, *args, **kwargs):
    await self.map_modules("on_reaction_remove", args, kwargs)

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
        logger.debug(f"{module.name} captured the [{func_name}] event.")
        break
      if not isinstance(result, bool):
        ValueError(
          f"The module {module.name} did not dispatch correctly "
          f"for the function {func_name}. Expected bool, got {type(result)}."
        )

  async def load_everythin(self, message, guild=None):
    if guild is None:
      guild = message.channel.guild
    self.sync_manager.servers.add(guild)
    with suno.database.Session() as session:
      suno.database.create_server(guild)
    await self.load_servers_roles(message, guild)

  async def load_servers_roles(self, message, guild):
    roles = await guild.fetch_roles()
    i = 0
    for role in roles:
      if role.name not in self.config.ROLE_NAME_TO_CODE.get(guild.id, {}):
        logger.warning(f"Unknown role: {role.name}")
        continue
      self.load_role(guild, role)
      logger.info(f"Role {role.name} loaded from {guild.name}.")
      i += 1
    if message is not None:
      await self._modules[0].send_message(
        message.channel,
        f"Nombre de roles chargés: {i}"
      )

  def load_role(self, guild, role):
      self.config.ROLES.setdefault(guild.id, {})[
        self.config.ROLE_NAME_TO_CODE[guild.id][role.name]
      ] = role
      suno.database.create_role(role, guild)

  def get_role(self, guild, role_code):
    return self.config.ROLES.setdefault(guild.id, {}).get(role_code)

  def set_dev_mode(self, print_stdout=True):
    if not self.dev:
      self.dev = True
      if print_stdout:
        suno.utils.add_stdout_handler(logger)
        suno.utils.add_stdout_handler(suno.database.database_logger)
      suno.database.database_logger.setLevel(logging.DEBUG)
      logger.setLevel(logging.DEBUG)
      logger.debug(f"Dev mode activated for client.")
      for module in self._modules:
        module.set_dev_mode(print_stdout=print_stdout)

  def run(self, dev=False, *args, **kwargs):
    if dev:
      self.set_dev_mode(*args, **kwargs)
    super().run(self.token)
