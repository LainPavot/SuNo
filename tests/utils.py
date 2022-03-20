


import pytest
import asyncio

import ticu.app
import ticu.config
import ticu.modules


import discord
import discord.flags
import discord.ext.test as dpytest

async def kill_bot(bot):
  await asyncio.sleep(.1)
  bot._closed = True
  await bot.http.close()
  bot._ready.clear()
  await asyncio.sleep(.1)

@pytest.fixture
def bot(event_loop, capsys):
  intents = discord.Intents.all()
  app = ticu.app.App(intents=intents, event_loop=event_loop)
  for module in (
    ticu.modules.RaidHandler,
    ticu.modules.NewMembers,
  ):
    module = module(app)
    app.register(module)
  app.set_dev_mode(print_stdout=False)
  dpytest.configure(app, num_guilds=20)
  return app