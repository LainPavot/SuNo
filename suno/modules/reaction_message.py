
import discord

# import suno.command as cmd
import suno.database
import suno.module


def pair_of_reaction_role(message:discord.Message, args):
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

  command_info = dict(
    gives_role=dict(
      all_args=(pair_of_reaction_role, ),
      # all_args=(
      #   cmd.sliced(0, 1)(cmd.are(suno.command.args.string)),
      #   cmd.sliced(1, sep=2)(cmd.are(suno.command.args.role)),
      #   cmd.sliced(2, sep=2)(cmd.are(suno.command.args.string)),
      #   (lambda _:len(_) > 2 and not len(_)%2)
      # ),
      before_args=lambda x:(x["message"], ),
      help=(
        "Assigne/enleve des roles au personnes, lorsqu'elles réagissent "
        f"selon les emotes données:\n"
        f" !{command_prefix} gives_role 'Texte que le bot va afficher'"
        " emote 'role associé' emote2 'role associé2' ... "
        "\nFaites bien attention à mettre les noms des roles entre guillemets"
        " si ceux-si sont en plusieurs mots!"
      ),
      perms=dict(
        role=("ROLE_CONFIANCE_HAUTE", )
      ),
    ),
    vote=dict(
      all_args=(
        lambda cmd:all(map(suno.command.args.string.__eq__, cmd[:2])),
        lambda cmd:len(cmd) in (2, 3),
      )
    ),
    vote_donner_role_confiance_haute=dict(
      all_args=(
        suno.command.args.mention,
      ),
      help="Déclanche un vote pour assinger le role de \"{role_confiance_haute.name}\""
    )
  )

  base_vote_emotes = "✅", "❌", "❔", "⚪", "⏱"
  base_vote_emote_expl = "\n".join((
    f"{base_vote_emotes[0]} = oui",
    f"{base_vote_emotes[1]} = non",
    f"{base_vote_emotes[2]} = je ne sais pas",
    f"{base_vote_emotes[3]} = vote blanc",
    f"{base_vote_emotes[4]} = repousser à plus tard",
  ))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    ## the command name to assign the "turquoise" role should be
    ## _command_vote_turquoise, so, people would type "!react vote_turquoise"
    ## To start the vote. BUT! (lol) the role name "turquoise" is prone to
    ## changes. So we need a generic name: vote_donner_role_confiance_haute
    ## BUT! (re-lol) this is too long, and people will want a shorted name.
    ## SO! (Sick ov' that lol) we assign an alternative name, generated from
    ## the config file, and we keep the most self-explainatory name for the
    ## function name itself.
    self.command_info[
      f"vote_{self.config.GENERIC_NAME_HAUTE_CONFIANCE}"
    ] = self.command_info["vote_donner_role_confiance_haute"]
    setattr(
      self,
      f"vote_{self.config.GENERIC_NAME_HAUTE_CONFIANCE}",
      self._command_vote_donner_role_confiance_haute
    )
    self.gives_role_cache = {}
    self.vote_cache = {}

  async def on_reaction_add(self, reaction:discord.Reaction, user:discord.User):
    if user.bot:
      return False
    message = reaction.message
    for handler in ("handle_role", "handle_vote"):
      if await getattr(self, handler)(reaction, user, message):
        return True
    return False

  async def handle_vote(
    self,
    reaction:discord.Reaction,
    user:discord.User,
    message:discord.Message
  ):
    if not (counters := self.vote_cache.get(message.id)):
      return False
    if reaction.emoji not in counters["emotes"]:
      return False
    counters["users"][user.id] = reaction.emoji
    await reaction.remove(user)
    if len(counters["users"]) >= counters["end"]:
      await self.end_vote(message, counters)
    return True

  async def end_vote(self, message:discord.Message, counters):
    all_votes = list(counters["users"].values())
    nb_total_votes = len(all_votes)
    votes = {
      emoji: all_votes.count(emoji)
      for emoji in counters["emotes"]
    }
    recap = '\n'.join([
      f"{emoji}: {result} ({result / nb_total_votes * 100}%)"
      for emoji, result in votes.items()
    ])
    cmd = counters["commande"]
    await message.edit(
      content=(
        f"Vote pour terminé.\n"
        "```markdown\n"
        "Issue du vote \n"
        f"===\n"
        f"{recap}\n"
        f"\n"
        f" * Nombre total de votes: {nb_total_votes}\n"
        f" * commande: {cmd if isinstance(cmd, str) else '<internal command>'}\n"
        f"```"
      )
    )

  async def handle_role(
    self,
    reaction:discord.Reaction,
    user:discord.User,
    message:discord.Message
  ):
    if not (role_manager := self.gives_role_cache.get(message.id)):
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
    args = args[1:]
    emote_to_role = {
        emote: role
      for emote, role in zip(args[::2], args[1::2])
    }
    if not await self.add_message_to_watch(
      "gives_role",
      self_msg,
      emote_to_role,
      show_emotes=True
    ):
      await self_msg.delete()
    else:
      await message.delete()
    return True

  async def _command_vote_donner_role_confiance_haute(
    self, message, command, args
  ):
    role = suno.utils.code_to_role(
      self.config,
      guild,
      suno.config.ROLE_CONFIANCE_HAUTE
    )
    return await self.create_role_vote(message, command, args, role)
  
  async def create_role_vote(self, message, command, args, role):
    pass


  async def _command_vote(self, message, command, args, end_count=-1):
    emotes = self.base_vote_emotes
    text = f"Vote pour: {args[0]}\n{self.base_vote_emote_expl}"
    if len(args) == 3:
      try:
        end_count = int(args[2])
      except ValueError:
        self.send_message(
          message.channel,
          f"\"{args[2]}\" (nombre de votes max) n'est pas un "
          "nombre entier."
        )
    await self.create_vote(
      text,
      emotes,
      message.channel,
      command=args[1],
      end_vote=end_count
    )

  async def create_vote(
    self,
    text,
    emotes,
    channel,
    command,
    end_vote,
  ):
    self_msg = await self.send_message(
      channel,
      text,
      return_message=True
    )
    emote_to_count = dict(
      emotes=emotes,
      users=dict(),
      commande=command,
      end_vote=end_vote
    )
    await self.add_message_to_watch(
      "vote",
      self_msg,
      emote_to_count,
      show_emotes=emotes
    )

  async def add_message_to_watch(self, kind, message, value, show_emotes=False):
    if isinstance(show_emotes, bool):
      if show_emotes:
        emotes = value.keys()
      else:
        emotes = []
    else:
      emotes = show_emotes
    for emote in emotes:
      try:
        await message.add_reaction(emote)
      except:
        await self.send_message(
          message.channel,
          f"Désolæ, mais il n'est pas possible de réagire "
          f"avec \"{emote}\"..."
        )
        return False
    getattr(self, f"{kind}_cache")[message.id] = value
    return True