

import discord

import ticu.database


class RoleSync:

  prefix = "_sync_role_"
  syncable_role_action = "add", "remove"

  async def _sync_role_remove(self, member:discord.Member, role:discord.Role):
    await member.remove_roles(role)
    with ticu.database.Session() as session:
      for role in member.roles:
        ticu.database.remove_role(member, role, session)
    return True

  async def _sync_role_add(self, member:discord.Member, role:discord.Role):
    await member.add_roles(role)
    with ticu.database.Session() as session:
      for role in member.roles:
        ticu.database.assign_role(member, role, session)
    return True

