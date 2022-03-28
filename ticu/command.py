

import collections


_command_args = ("string", "mention", )
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

__all__ = [
  "args",
  "equals",
  "contains",
]