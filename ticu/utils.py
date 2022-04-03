

## fix to prevent attr error in logger.addHandler
from logging import handlers

import contextlib
import logging
import os
import re
import sys
import typing

import discord
import discord.errors


class PIDManager(contextlib.ContextDecorator):

  def __init__(self, pidfile, on_exists_callback=None):
    self.on_exists_callback = on_exists_callback
    self._pidfile = None
    super().__init__()
    self.pidfile = pidfile

  @property
  def pidfile(self):
    return self._pidfile

  @pidfile.setter
  def pidfile(self, pidfile):
    if self._pidfile is not None:
      ## if the pidfile is changed for another location
      os.unlink(self.pidfile)
    self._pidfile = pidfile
    if self.pidfile is not None:
      pid = self.create_pid_file()
      if pid is not None and self.on_exists_callback is not None:
        self.on_exists_callback(pid)
        # raise RuntimeError(f"This bot is already running - pid: {pid}.")

  def create_pid_file(self):
    if os.path.exists(self.pidfile):
      with open(self.pidfile, 'r') as pidfile:
        return pidfile.read()
    with open(self.pidfile, 'w') as pidfile:
      pidfile.write(f"{os.getpid()}")
    return None

  def __enter__(self):
    pass

  def __exit__(self, *exc):
    if self.pidfile is not None:
      os.unlink(self.pidfile)



def get_formater():
  return logging.Formatter(
    "[%(name)-16s-%(levelname)-5s %(asctime)s] %(message)s",
    "%Y-%m-%d %H:%M:%S"
  )

def get_logger(name, filename=None, debug=False, noprint=True):
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG if debug else logging.INFO)

  formater = get_formater()

  if not noprint:
    add_stdout_handler(logger)

  if filename:
    try:
      file_stream_handler = logging.handlers.RotatingFileHandler(
        filename, maxBytes=10_000_000
      )
      file_stream_handler.setFormatter(formater)
      logger.addHandler(file_stream_handler)
    except AttributeError as e:
      pass
  return logger

def add_stdout_handler(logger):
  stream_handler = logging.StreamHandler(sys.stdout)
  stream_handler.setFormatter(get_formater())
  logger.addHandler(stream_handler)

async def user_from_mention(client, mention, logger=None, guild=None):
  if re.match(r"<@&\d{18}>", mention):
    return None
  match = re.search(r"\d{18}", mention)
  user_id = match[0]
  logger and logger.debug(f"Fetching user of ID {user_id}")
  if guild:
    return await guild.fetch_member(int(user_id))
  else:
    return await client.fetch_user(int(user_id))

def extract_id(message, as_int=False):
  if as_int:
    try:
      return int(extract_id(message))
    except:
      return None
  try:
    return re.search(r"\d{18}", message)[0]
  except:
    return None

def role_to_code(conf, guild:discord.Guild, role):
  conf.ROLE_NAME_TO_CODE

def code_to_role_name(conf, guild:discord.Guild, code):
  conf.ROLE_CODE_TO_NAME

def role_name_to_role(guild, role_name):
  for role in guild.roles:
    if role_name == role.name:
      return role
  return None

def role_id_to_role(guild, role_id):
  for role in guild.roles:
    if role_name == role.id:
      return role
  return None

def role_to_code_to_role(
  conf,
  input_guild:discord.Guild,
  role:discord.Role,
  output_guild:discord.Guild
) -> typing.Optional[discord.Role]:
  if not (code := role_to_code(conf, input_guild, role)):
    print(
      f"Role {role.name}:{role.id} is not known by the bot."
      " Please, add it to the conf file."
    )
    return None
  if not (output_role_name := code_to_role_name(conf, output_guild, code)):
    print(
      f"Role {role.name}:{role.id} does not exists on the other guild."
      f" Please, add the translation to {output_guild.name} conf file."
    )
    return None
  if not (output_role := role_name_to_role(output_guild, output_role_name)):
    print(
      f"Role {role.name}:{role.id} does not exists on the other guild."
      f" Please, create it in the guild {output_guild.name}."
    )
    return None
  return output_role