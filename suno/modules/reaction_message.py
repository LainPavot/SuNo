
import discord

import suno.command
import suno.database
import suno.module


def pair_of_reaction_role(message:discord.Message, args, parsed):
  args = args[1:]
  if not args:
    return False
  if len(args) % 2 != 0:
    return False
  for emote, role in zip(args[::2], args[1::2]):
    if not suno.command.arg_is_role(message.channel.guild, role):
      print(message.channel.guild.roles)
      return f"'{role}' n'est pas un nom ni un identifiant de role reconnu."
  return True


class ReactionMessage(suno.module.SuNoModule):

  name = "ReactionMessage"

  command_prefix = "react"
  module_help = (
    "Ce module fournit un ensemble de commandes relatives aux réactions,"
    " qui déclancheront des actions données."
  )

  test_command_info = dict(
    gives_role=dict(
      all_args=(pair_of_reaction_role, ),
      before_args=lambda x:(x["message"], ),
      help=(
        "Assigne/enleve des roles au personnes, lorsqu'elles réagissent "
        f"selon les emotes données:\n"
        f" !{command_prefix} gives_role 'Texte que le bot va afficher'"
        " emote 'role associé' emote2 'role associé2' ... "
        "\nFaites bien attention à mettre les noms des roles entre guillemets"
        " si ceux-si sont en plusieurs mots!"
      ),
      # perms=dict(
      #   role=("TUTU", )
      # ),
    )
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.cache = {}

  async def on_reaction_add(self, reaction:discord.Reaction, user:discord.User):
    if user.bot:
      return False
    message = reaction.message
    if not (role_manager := self.cache.get(message.id)):
      return False
    self.logger.info(
      f"{user.name} add reacted to {message.content} with {reaction.emoji}."
    )
    if not (role_name := role_manager.get(reaction.emoji)):
      return False
    self.logger.info(
      f"{reaction.emoji} is recognized among expected emotes."
    )
    if not (member := message.channel.guild.get_member(user.id)):
      self.logger.info(
        f"The user exited the server before we could assign the role. Fishy...."
      )
      return False
    await self.assign_or_remove_role(member, role_name)
    await reaction.remove(user)
    return True

  async def assign_or_remove_role(self, member:discord.Member, role_name:str):
    roles = await member.guild.fetch_roles()
    if not (filtered := [role for role in roles if role.name == role_name]):
      return False
    role = filtered[0]
    for curent_role in member.roles:
      if curent_role == role:
        return await self.manage_role("remove", member, role)
    return await self.manage_role("add", member, role)

  async def _command_gives_role(self, message, command, args):
    self_msg = await message.channel.send(args[0])
    for emote, role in zip(args[1::2], args[2::2]):
      try:
        await self_msg.add_reaction(emote)
      except:
        await self_msg.delete()
        return await self.send_message(
          message.channel,
          f"Désolæ, mais il n'est pas possible de réagire "
          f"avec \"{emote}\"..."
        )
    await message.delete()
    self.add_message_to_watch(self_msg, args[1:])

  def add_message_to_watch(self, message, args):
    self.cache[message.id] = {
      emote: role
      for emote, role in zip(args[::2], args[1::2])
    }