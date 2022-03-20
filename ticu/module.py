

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
    return "\n".join((
      f"{self.name}",
      f"===",
      f"{self.module_help}",
      "\nCommandes:\n * "+"\n * ".join(command for command in self.command_info),
      f"",
      f"{commands_help}",
    ))