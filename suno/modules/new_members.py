

import discord

import suno.command
import suno.database
import suno.module


class NewMembers(suno.module.SuNoModule):

  name = "NewMembers"

  command_prefix = "welcome"

  test_command_info = dict(
    to=dict(
      args=(suno.command.contains(suno.command.args.mention), )
    )
  )

  welcome_message = """
  {user.mention}, bienvenu sur {guild.name}.
  """

  welcome_back_message = """
  {user.mention}, bon retour sur {guild.name}.
  """

  async def on_ready(self, *args, **kwargs):
    await super().on_ready(*args, **kwargs)
    print(suno.database.Session())
    return False

  async def on_member_join(self, member):
    if suno.database.has_member(member):
      handler = self.handle_member_coming_back
    else:
      handler = self.handle_member_first_coming
    no_process = await handler(member)
    self.logger_debug_function(f"No process flag is {no_process}")
    return no_process

  async def handle_member_coming_back(self, member):
    if suno.database.has_auto_ban(member):
      await self.ban_member(member)
      self.logger.info(f"Member {member.mention} has autoban flag: banned.")
      return True
    else:
      self.logger.debug(f"Member {member.mention} does not have the autoban flag ")
    if suno.database.has_auto_kick(member):
      await self.kick_member(member)
      self.logger.info(f"Member {member.mention} has autokick flag: kicked.")
      return True
    else:
      self.logger.debug(f"Member {member.mention} does not have the autokick flag ")
    self.logger.info(f"Old member {member.mention} has re-joined the server.")
    await self.send_welcome_message(member, back=True)
    await self.reassign_roles(member)
    return False

  async def handle_member_first_coming(self, member):
    self.logger.info(f"New member {member.mention} has joined the server.")
    suno.database.create_member(member)
    await self.send_welcome_message(member)
    return False

  async def send_welcome_message(self, member, guild=None, back=False):
    if guild is None:
      guild = member.guild
    if back:
      message = self.welcome_back_message
    else:
      message = self.welcome_message
    to_send = message.format(user=member, guild=guild)
    if not await self.send_to_system_channel(guild, to_send):
      if (channel := self._find_appropriate_random_channel(guild)):
        return await self.send_message(channel, to_send)
    return False

  def _find_appropriate_random_channel(self, guild):
    channels = [
      channel
      for channel in guild.channels
      if not isinstance(channel, (discord.CategoryChannel, discord.VoiceChannel))
    ]
    for is_fine_channel in (
      lambda channel:channel.name.lower() in ("général", "general"),
      lambda channel:"général" in channel.name.lower(),
    ):
      for channel in channels:
        if is_fine_channel(channel):
          return channel
    return None

  async def reassign_roles(self, member):
    self.logger.warning(f"{self.name}-reassign_roles not implemented")

  async def _command_to(self, message, command, args):
    user = await suno.utils.user_from_mention(
      self._app,
      args[0],
      logger=self.logger,
      # guild=message.channel.guild
    )
    if user is None:
      return False
    member = await message.channel.guild.fetch_member(user.id)
    return await self.on_member_join(member)
    return await self.send_welcome_message(
      user,
      guild=message.channel.guild
    )

