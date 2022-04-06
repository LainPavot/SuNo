
import suno.command
import suno.database
import suno.module


class DebugModule(suno.module.SuNoModule):

  name = "DebugModule"

  command_prefix = "info"
  module_help = (
    "Module de debug et d'informations. \n"
    " Permet d'afficher plein d'info utiles dans le cadre du debug, ou pour"
    " informer les personnes des informations que la bot a sur ces personnes."
  )

  test_command_info = dict(
    db=dict(args=tuple()),
    user=dict(args=suno.command.args.mention)
  )

  async def _command_user(self, message, command, args):
    return True

  async def _command_db(self, message, command, args):
    with suno.database.Session() as session:
      servers = session.query(suno.database.Server).all()
      server_list_info = "\n".join(
        self._compile_info(obj, main_attr="name", attributes={"id":"id"})
        for obj in servers
      )
      servers_info = [
        (server, *self._produce_server_info(message, server))
        for server in servers
      ]
    await self.send_message(
      message.channel,
      f"```markdown\n"
      f"List des Info sur les serveurs\n"
      f"===\n"
      f"{server_list_info}\n"
      f"```"
    )
    for server, member_list_info, role_list_info in servers_info:
      await self.send_message(
        message.channel,
        f"```markdown\n"
        f"{server.name} - members info\n"
        f"===\n"
        f"{member_list_info}\n"
        f"```"
      )
      await self.send_message(
        message.channel,
        f"```markdown\n"
        f"{server.name} - roles info\n"
        f"===\n"
        f"{role_list_info}\n"
        f"```"
      )

  def _produce_server_info(self, message, server):
    # with suno.database.Session() as session:
    #   server = session.query(suno.database.Server).filter_by(id=server.id)
    members = server.members
    member_list_info = "\n".join(
      self._compile_info(
        obj,
        main_attr="id",
        attributes={
          "kicked":"kicked",
          "banned":"banned",
          "auto_kick":"auto_kick",
          "auto_ban":"auto_ban",
        }
      )
      for obj in members
    )
    role_list_info = "\n".join(
      self._compile_info(
        obj,
        main_attr="name",
        attributes={
          "id": "id",
          "member count": lambda role:len(role.members)
        }
      )
      for obj in server.roles
    )
    return member_list_info, role_list_info

  def _compile_info(self, obj, main_attr, attributes):
    return "\n".join((
      f" - {getattr(obj, main_attr)}:", *(
        f"   - {key}: {getattr(obj, val) if isinstance(val, str) else val(obj)}"
        for key, val in attributes.items()
      ),
    ))
