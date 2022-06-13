

import datetime

import discord

import suno.command
import suno.database
import suno.module
import suno.utils


class NewMembers(suno.module.SuNoModule):

  name = "NewMembers"

  command_prefix = "welcome"

  test_command_info = dict(
    to=dict(
      args=(suno.command.contains(suno.command.args.mention), )
    )
  )

  delay_after_upgrade_confidence = datetime.timedelta(days=30)
  delay_after_upgrade_confidence_string = "30 jours"

  welcome_message = """
  Bonjour et bienvenue {user.mention} !
Pour pouvoir rentrer, nous te demandons de nous faire une petite présentation, qui devra inclure où tu as connu le serveur, pourquoi tu l'as rejoint, une confirmation que tu as lu et accepté les règles, et n'importe quoi d'autre que tu jugeras utile
Nous te demandons de mettre également tes pronoms dans ton pseudo
Merci et bonne journée
  """

  welcome_back_message = """
  Bonjour {user.mention}, et bon retour sur {guild.name} !
  """

  async def on_ready(self, *args, **kwargs):
    await super().on_ready(*args, **kwargs)
    return False

  async def on_member_join(self, member):
    if suno.database.has_member(member):
      handler = self.handle_member_coming_back
    else:
      handler = self.handle_member_first_coming
    no_process = await handler(member)
    self.logger_debug_function(f"No process flag is {no_process}")
    return no_process

  async def on_message(self, message, *args, **kwargs):
    member = message.author
    if (
      not hasattr(member, "joined_at")
      or not (joined_at := member.joined_at)
    ):
      return ## not a guild member; DM
    lapse = datetime.datetime.now() - joined_at
    if lapse < self.delay_after_upgrade_confidence:
      return ## joined less than 30 days ago
    new_role_name = suno.utils.code_to_role_name(
      self.config,
      member.guild,
      self.config.ROLE_CONFIANCE_MOYENNE
    )
    for curent_role in member.roles:
      if curent_role.name == new_role_name:
        ## the user has already this role, baka!
        return

    roles = await member.guild.fetch_roles()
    if not (filtered := [role for role in roles if role.name == new_role_name]):
      self.logger.warning(
        f"Tried to find role {new_role_name} on server {member.guild.name}, "
        "but could not find it!"
      )
      return
    role = filtered[0]
    await message.reply(
      f"Félicitation! Ça fait {self.delay_after_upgrade_confidence_string} "
      f"que tu es sur le serveur!\n"
      f"Te voilà maintenant {role.name} {suno.utils.random_heart()}"
    )
    await self.manage_role("add", member, role)

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
      # message = self.config.WELCOME_MESSAGES.get(
      #   member.guild.id,
      #   self.config.DEFAULT_WELCOME_MESSAGE
      # )
    else:
      # message = self.welcome_message
      message = self.config.WELCOME_MESSAGES.get(
        member.guild.id,
        self.config.DEFAULT_WELCOME_MESSAGE
      )
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

