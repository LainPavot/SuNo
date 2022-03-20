
import pytest
import asyncio

import ticu.app
import ticu.config
import ticu.modules

import discord
import discord.flags
import discord.ext.test as dpytest

from .utils import bot, kill_bot


# intents = discord.Intents.all()


# async def kill_bot(bot):
#   await asyncio.sleep(.1)
#   bot._closed = True
#   await bot.http.close()
#   bot._ready.clear()
#   await asyncio.sleep(.1)

# @pytest.fixture
# def bot(event_loop, capsys):
#   app = ticu.app.App(intents=intents, event_loop=event_loop)
#   for module in (
#     ticu.modules.NewMembers,
#   ):
#     module = module(app)
#     app.register(module)
#   app.set_dev_mode(print_stdout=False)
#   dpytest.configure(app, num_guilds=2)
#   return app

@pytest.mark.asyncio
async def test_welcome_one(bot, capsys):
  member = await dpytest.member_join(0, discrim=1)
  await asyncio.sleep(.1)
  guild = dpytest.runner._cur_config.guilds[0]
  await asyncio.sleep(.1)
  assert dpytest.verify().message().contains().content(
    f"Welcome {member.mention} to {guild.name}!"
  )
  await kill_bot(bot)

@pytest.mark.asyncio
async def test_welcome_three(bot, capsys):
  for i in range(2, 5):
    member = await dpytest.member_join(0, discrim=i)
    guild = dpytest.runner._cur_config.guilds[0]
    await asyncio.sleep(0.1)
    assert dpytest.verify().message().contains().content(
      f"Welcome {member.mention} to {guild.name}!"
    )
  await asyncio.sleep(.1)
  await kill_bot(bot)
