


import asyncio
import time

import ticu.module

class RaidHandler(ticu.module.TiCuModule):

  name = "RaidHandler"
  command_prefix = "raid"
  module_help = (
    "Ce module tente de décter les raids, en évaluant la fréquence"
    " à laquelle des personnes joignent le serveur. En cas de raid, il"
    " désactive les liens d'invitations et bannis de façon"
    " préventive toutes les personnes qui essaient de rejoindre le"
    " serveur."
  )
  command_info = dict(
    on=dict(
      help=(
        "Activer le mode raid: Désactiver les invitations, autoban les"
        " personnes qui rejoignent le serveur."
      ),
      perms=dict(
        role=("ROLE_CONFIANCE_HAUTE", )
      ),
    ),
    off=dict(
      help=(
        "Desactiver le mode raid."
      ),
      perms=dict(
        role=("ROLE_CONFIANCE_HAUTE", )
      ),
    ),
    status=dict(
      help=(
        "Obtenir les status du module anti-raid."
      ),
    ),
  )

  test_command_info = dict(
    
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.last_join = {}
    self.suspicious_members = {}
    self.previous_member_to_join = {}
    self.alert_message_list = {}
    self.raid_mode = False

  async def on_member_join(self, member):
    guild = member.guild
    last_join = self.last_join.get(guild.id, 0)
    if (
      self.raid_mode
      or time.time() - last_join < self.config.SUSPICIOUS_JOIN_FREQUENCY
    ):
      await self.handle_raid_member(member)
      ## No other module should handle this arival if this is a raid.
      return True
    self.last_join[guild.id] = time.time()
    self.previous_member_to_join[guild.id] = member
    return False

  async def handle_raid_member(self, member):
    guild = member.guild
    suspicious_members = self.suspicious_members.setdefault(guild.id, [])
    if len(suspicious_members) == 0:
      suspicious_members.append(self.previous_member_to_join)
    suspicious_members.append(member)
    if not self.raid_mode:
      await self.activate_raid_mode(guild)
    else:
      self.logger.info(f"New raider detected: {member.mention}")
      self.alert_message_list.setdefault(member.guild.id, [])
      ## we update the alert messages for each new raid person
      while not self.alert_message_list[member.guild.id]:
        ## We wait for the first message to be sent in the gackground task.
        ## Executed only when three members join at a very high frequency.
        await asyncio.sleep(1)
      await self.alert_everyone(guild)

  async def activate_raid_mode(self, guild):
    self.logger.info("Raid mode activated")
    self.raid_mode = True
    await self.deactivate_invite_message(guild)
    self.background_alert_everyone = self.loop.create_task(
      self.alert_everyone(guild)
    )

  async def deactivate_invite_message(self, guild):
    try:
      for invite in await guild.invites():
        await self.send_to_system_channel(guild, f"Suppression de l'invitation {invite.id}")
        await invite.delete()
      else:
        await self.send_to_system_channel(guild, "Aucune invitation active")
    except NotImplementedError:
      pass
      ## #The test framework did not implement invites mecanisms...

  async def deactivate_raid_mode(self, guild):
    self.raid_mode = False
    await self.delete_alerte_messages(guild)
    await self.reactivate_invites(guild)

  async def reactivate_invites(self, guild):
    await self.send_to_system_channel(
      guild,
      "\n".join((
        "Le mode raid du bot a été désactivé.",
        "N'oubliez pas de recréer des invitations."
      ))
    )

  async def delete_alerte_messages(self, guild):
    self.alert_message_list.setdefault(guild.id, [])
    while self.alert_message_list[guild.id]:
      await self.alert_message_list[guild.id].pop().delete()

  async def alert_everyone(self, guild):
    content = (
      "Ces personnes on rejoint le serveur dans des faibles"
      + "intervales de temps:\n"
      + "\n".join(member.mention for member in self.suspicious_members)
    )
    self.alert_message_list.setdefault(guild.id, [])
    if not self.alert_message_list[guild.id]:
      await self.new_alert_message(content, guild)
    else:
      await self.update_alert_message(
        self.alert_message_list[guild.id],
        content
      )
    return False

  async def new_alert_message(self, content, guild):
    self.alert_message_list.setdefault(guild.id, [])
    for role in (
      self.config.TUTU_ROLES,
      self.config.PHO_PLUS_ROLES,
      self.config.PHO_ROLES,
    ):
      message = await self.send_reaction_message(
        content,
        guild,
        ping=role[guild.id],
        callback=self.handle_alert_message_reaction
      )
      self.alert_message_list[guild.id].append(message)
      await asyncio.sleep(10)
      ## raid may be deactivated while we are sending messages
      ## to pho + and pho.
      if not self.raid_mode:
        break

  async def handle_alert_message_reaction(self, message, reaction):
    if reaction.id == self.config.INFIRM_RAID:
      await self.deactivate_raid_mode()

  async def _command_on(self, message, command, args):
    await self.activate_raid_mode(message.channel.guild)
    await self._command_status(message, "", ())

  async def _command_off(self, message, command, args):
    await self.deactivate_raid_mode(message.channel.guild)
    await self._command_status(message, "", ())

  async def _command_status(self, message, command, args):
    await self.send_message(
      message.channel,
      f"{self.name} status: {'activé' if self.raid_mode else 'en veille'}"
    )
