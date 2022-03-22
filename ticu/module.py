

import asyncio
import inspect
import logging
import re

import ticu.database
import ticu.utils

class TiCuModule:

  name = "TiCuModule"
  command_prefix = name
  module_help = (
    "L'aide de ce module n'a pas été rédigée, n'hésitez pas"
    "à contacter Lainou#2122 ou tout autre personne du dev' pour la rédiger, "
    "ou pour vous l'expliquer."
  )
  command_info = dict(
    help=dict()
  )

  def __hash__(self):
    return hash(f"TiCuModule-{self.name}")

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
    self.command_info.setdefault("help", dict(help="Obtenir l'aide de ce module"))
    self.check_integrity()

  def check_integrity(self):
    missing_method = ", ".join(
      f"_command_{command}"
      for command in self.command_info
      if not hasattr(self, f"_command_{command}")
    )
    if not missing_method:
      return
    self.early_failure()
    message = "\n".join((
      f"Integrity problems has been encountered in the {self.name} module.",
      f"Missing methods: {missing_method}. Please implement them."
    ))
    self.logger.error(message)
    raise ValueError(f"Some integrity checks failed.\n{message}")

  def early_failure(self):
    ticu.utils.add_stdout_handler(self.logger)
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug("Early failure: logger outputs on stdout.")

  @property
  def config(self):
    return self._app.config

  @property
  def loop(self):
    return self._app.loop

  def set_dev_mode(self, print_stdout=True):
    if not self.dev:
      self.dev = True
      if print_stdout:
        ticu.utils.add_stdout_handler(self.logger)
      self.logger.setLevel(logging.DEBUG)
      self.logger.debug(f"Dev mode activated for module {self.name}.")

  async def on_ready(self, *args, **kwargs):
    self.logger.debug(f"Module {self.name} loaded and ready.")
    return False

  async def on_message(self, message, *args, **kwargs):
    self.logger_debug_function(f"Got message: {message.content}")
    return await self.handle_command(message)

  async def on_member_join(self, member, *args, **kwargs):
    self.logger_debug_function(f"New member just joined: {member.name}")
    return False

  async def ban_member(self, member):
    ticu.database.ban_member(member)
    await member.guild.ban(member)
    self.logger.debug(f"[discord] {member.mention} has been baned.")

  async def ban_member(self, member):
    ticu.database.kick_member(member)
    await member.guild.kick(member)
    self.logger.debug(f"[discord] {member.mention} has been kicked.")

  async def send_to_system_channel(self, guild, to_send):
    if guild.system_channel is not None:
      self.logger.debug(f"[discord] Sending message \"{to_send}\" in {guild.system_channel.name}.")
      await guild.system_channel.send(to_send)
      return True
    else:
      self.logger.debug(f"There is no system channel. Cannot send message.")
    return False

  async def send_message(self, channel, to_send):
    self.logger.debug(f"[discord] Sending message \"{to_send}\" in {channel.name}.")
    await channel.send(to_send)
    return True

  async def send_reaction_message(
    self,
    content,
    guild,
    ping=None,
    callback=None
  ):
    pass

  def logger_debug_function(self, message):
    self.logger.debug(f"[{inspect.stack()[1][3]}] - {message}")

  async def handle_command(self, message):
    content = re.sub(r"\s{2,}", " ", message.content.strip())
    if content == "!help":
      await self._command_all_helps(message)
      return True
    if not content.startswith(f"!{self.command_prefix} "):
      return False
    module, command, *args = content.split(" ")
    if command not in self.command_info:
      return await self.send_message(
        message.channel,
        f"Commande inconnue: {command}"
      )
    self.logger_debug_function(f"Command matches {self.name}:{command}.")
    await self.run_command_check_perm(message, command, tuple(args))
    return True

  async def run_command_check_perm(self, message, command, args):
    if not self.check_perms(message.author, command):
      return await self.send_message(
        message.channel,
        "Vous n'avez pas l'autorisation de lancer cette commande."
      )
    if (command_info := self.command_info.get(command, None)) is None:
      return await self.send_message(
        message.channel,
        (
          f"Cette commande n'existe pas."
          f"Envoyez !{self.command_prefix} help pour obtenir de l'aide."
        )
      )
    handler = getattr(self, f"_command_{command}")
    await handler(message, command, args)

  def get_role(self, *args, **kwargs):
    return self._app.get_role(*args, **kwargs)

  def check_perms(self, user, command):
    command_info = self.command_info[command]
    if not (roles := command_info.get("perms", {}).get("role")):
      return True
    roles = set([self.get_role(user.guild, role) for role in roles])
    return set(user.roles) & roles

    return True

  async def _command_help(self, message, command, args):
    await self.send_message(
      message.channel,
      self._build_module_md_help()
    )

  async def _command_all_helps(self, message):
    await self.send_message(
      message.channel,
      self._build_all_modules_md_help()
    )

  def _build_module_md_help(self):
    return "\n".join((
      f"```markdown",
      self._build_module_raw_help(),
      f"```",
    ))

  def _build_all_modules_md_help(self):
    return "\n".join((
      "```markdown",
      "\n".join(
        module._build_module_raw_help()
        for module in self._app._modules
      ),
      "```",
    ))

  def _build_module_raw_help(self):
    commands_help = "\n".join(
      f"{name}\n---\n{self.command_info[name].get('help', '')}\n"
      for name in self.command_info
    )
    commandes_with_perm = [
      f"{command} - {' - '.join(value.get('perms', {}).get('role', ('no perm', )))}"
      for command, value in self.command_info.items()
    ]
    return "\n".join((
      f"{self.name}",
      f"===",
      f"{self.module_help}",
      f"\nPréfix de commande: !{self.command_prefix}",
      "\nCommandes:\n * "+"\n * ".join(commandes_with_perm),
      f"",
      f"{commands_help}",
    ))