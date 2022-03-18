

import ticu.module
import ticu.database


class NewMembers(ticu.module.TiCuModule):

  name = "NewMembersModule"

  async def on_ready(self, *args, **kwargs):
    await super().on_ready(*args, **kwargs)
    print(ticu.database.Session())
    return False

  async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
      to_send = f"Welcome {member.mention} to {guild.name}!"
      await guild.system_channel.send(to_send)
    return False
