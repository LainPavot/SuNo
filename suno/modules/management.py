

import discord

import suno.command
import suno.database
import suno.module


class ManagementModule(suno.module.SuNoModule):

  name = "ManagementModule"

  command_prefix = "gestion"

  command_info = dict(
    suppr=dict(
      help=(
        "Supprimer le message du bot. Répondez au message avec cette"
        " commande"
      ),
      perms=dict(
        role=("ROLE_CONFIANCE_HAUTE", )
      ),
    )
  )
  async def _command_suppr(self, message, command, args):
    if not (refd := message.reference):
      msg = await self.send_tmp_message(
        message.channel,
        "Répondez à un de mes messages pour appliquer cette commande"
      )
      return False
    refm = await message.channel.fetch_message(refd.message_id)
    if refm.author.id != self._app.user.id:
      msg = await self.send_tmp_message(
        message.channel,
        "Ce n'est pas un message dont je suis l'aut·eur·rice."
      )
      return False
    await refm.delete()
    await message.delete()
    return True

