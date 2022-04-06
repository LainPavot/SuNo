

import discord

import suno.database


class SyncManager:
  servers = set()
  conf = {}


class RoleSync:

  prefix = "_sync_role_"
  syncable_role_action = "add", "remove"

  async def _sync_role_remove(
    self,
    member:discord.Member,
    role:discord.Role
  )->bool:
    await self.do_sync(self._remove_role, member, role)
    return True

  async def _remove_role(self, member, role):
    await member.remove_roles(role)
    suno.database.remove_role(member, role)

  async def _sync_role_add(
    self,
    member:discord.Member,
    role:discord.Role
  )->bool:
    await self.do_sync(self._add_role, member, role)
    return True

  async def _add_role(self, member, role):
    await member.add_roles(role)
    suno.database.assign_role(member, role)

  async def do_sync(self, callback, member, role):
    await callback(member, role)
    for server in SyncManager.servers:
      if server == member.guild:
        ## already treated above
        continue
      try:
        server_member = await server.fetch_member(member.id)
        server_role = suno.utils.role_to_code_to_role(
          SyncManager.conf, member.guild, role, server
        )
      except Exception as e:
        print(e)
        continue
      if server_role:
        await callback(server_member, server_role)
    return True

