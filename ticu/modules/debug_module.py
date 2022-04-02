
import ticu.command
import ticu.database
import ticu.module


class DebugModule(ticu.module.TiCuModule):

  name = "DebugModule"

  command_prefix = "debug"
  module_help = (
    "Module de debug et d'informations. \n"
    " Permet d'afficher plein d'info utiles dans le cadre du debug, ou pour"
    " informer les personnes des informations que la bot a sur ces personnes."
  )

  test_command_info = dict(
    db=dict(
      args=tuple()
    )
  )

  async def _command_db(self, message, command, args):
    with ticu.database.Session() as session:
      servers = session.query(ticu.database.Server).all()
      server_list_info = "\n".join(
        self._compile_info(obj, main_attr="name", attributes=("id", ))
        for obj in servers
      )
      servers_info = "\n\n".join(
        self._produce_server_info(message, server)
        for server in servers
      )
    await self.send_message(
      message.channel,
      f"```markdown\n"
      f"List des Info sur les serveurs\n"
      f"===\n"
      f"{server_list_info}\n"
      f"\n\n"
      f"{servers_info}"
      f"```"
    )

  def _produce_server_info(self, message, server):
    # with ticu.database.Session() as session:
    #   server = session.query(ticu.database.Server).filter_by(id=server.id)
    members = server.members
    member_list_info = "\n".join(
      self._compile_info(
        obj,
        main_attr="id",
        attributes=("kicked", "banned", "auto_kick", "auto_ban")
      )
      for obj in members
    )
    return (
      f"{server.name}\n"
      f"---\n"
      f"{member_list_info}\n"
    )

  def _compile_info(self, obj, main_attr, attributes):
    return "\n".join((
      f" - {getattr(obj, main_attr)}:", *(
        f"   - {attr}: {getattr(obj, attr)}"
        for attr in attributes
      ),
    ))
