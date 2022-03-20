
import ticu.module
import ticu.database


class NewMembers(ticu.module.TiCuModule):

  name = "NewMembers"

  async def on_ready(self, *args, **kwargs):
    await super().on_ready(*args, **kwargs)
    print(ticu.database.Session())
    return False

  async def on_member_join(self, member):
    if ticu.database.has_member(member):
      handler = self.handle_member_coming_back
    else:
      handler = self.handle_member_first_coming
    no_process = await handler(member)
    self.logger_debug_function(f"No process flag is {no_process}")
    return no_process

  async def handle_member_coming_back(self, member):
    if ticu.database.has_auto_ban(member):
      await self.ban_member(member)
      self.logger.info(f"Member {member.mention} has autoban flag: banned.")
      return True
    if ticu.database.has_auto_kick(member):
      await self.kick_member(member)
      self.logger.info(f"Member {member.mention} has autokick flag: kicked.")
      return True
    self.logger.info(f"Old member {member.mention} has re-joined the server.")
    await self.send_welcome_message(member)
    return False

  async def handle_member_first_coming(self, member):
    self.logger.info(f"New member {member.mention} has joined the server.")
    ticu.database.create_member(member)
    await self.send_welcome_message(member)
    return False

  async def send_welcome_message(self, member):
    guild = member.guild
    to_send = f"Welcome {member.mention} to {guild.name}!"
    sent = await self.send_to_system_channel(member.guild, to_send)
    if not sent:
      await self.send_message(member.guild.channels[0], to_send)
    return False
