

import collections

import ticu.utils


_command_args = ("string", "mention", "role_id", "role_name", "reaction")
args = collections.namedtuple(
  "CommandArgs",
  _command_args,
)(*range(len(_command_args)))

def contains(*_args):
  def contains_args(*args):
    return len(set(_args) & set(args)) > 0
  return contains_args

def equals(*_args):
  def eq_args(*args):
    return sorted(_args) == sorted(args)
  return eq_args

def arg_is_role(*args):
  return arg_is_role_id(*args) or arg_is_role_name(*args)

def arg_is_role_id(guild, arg):
  role_id = ticu.utils.extract_id(arg, as_int=True)
  return ticu.utils.role_id_to_role(guild, role_id) is not None

def arg_is_role_name(guild, arg):
  return ticu.utils.role_name_to_role(guild, arg) is not None

def arg_is_reaction_id(guild, arg):
  reaction_id = ticu.utils.extract_id(arg, as_int=True)
  return any(reaction_id == emoji.id for emoji in guild.emojis)

def split_args(content):
  try:
    return split_args_unsafe(content)
  except:
    return content

def split_args_unsafe(content):
  i = 0
  begin = 0
  def strip_val(val):
    if val[0] == val[-1] and val[0] in ("'", '"'):
      val = val.strip(val[0])
    return val
  while i < len(content):
    char = content[i]
    if char in ("'", '"'):
      i += 1
      while content[i] != char:
        i += 1
    i += 1
    if i >= len(content):
      yield strip_val(content[begin:i])
      return
    if content[i] in (" ", "\n"):
      yield strip_val(content[begin:i])
      begin = i+1
  yield content[begin:]

__all__ = [
  "args",
  "equals",
  "contains",
  "arg_is_role",
  "arg_is_role_id",
  "arg_is_role_name",
  "arg_is_reaction_id",
  "split_args",
]