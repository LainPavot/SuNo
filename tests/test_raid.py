
import pytest
import asyncio

import ticu.app
import ticu.config
import ticu.modules


import discord
import discord.flags
import discord.ext.test as dpytest

from .utils import bot


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

@pytest.mark.asyncio
async def test_one_member_joins(bot, capsys):
  member = await dpytest.member_join(0, discrim=1)
  await asyncio.sleep(.1)
  assert not bot._modules[0].raid_mode
  await kill_bot(bot)

@pytest.mark.asyncio
async def test_three_users_long_interval(bot, capsys):
  bot.config.SUSPICIOUS_JOIN_FREQUENCY = 0.1
  for i in range(2, 5):
    member = await dpytest.member_join(0, discrim=i)
    await asyncio.sleep(bot.config.SUSPICIOUS_JOIN_FREQUENCY+0.01)
  assert not bot._modules[0].raid_mode
  await kill_bot(bot)

@pytest.mark.asyncio
async def test_three_users_short_interval_diferent_servers(bot, capsys):
  bot.config.SUSPICIOUS_JOIN_FREQUENCY = 1
  for i in range(5, 8):
    member = await dpytest.member_join(i, discrim=i)

  await asyncio.sleep(.1)
  assert not bot._modules[0].raid_mode
  await kill_bot(bot)

@pytest.mark.asyncio
async def test_three_users_short_interval_same_server(bot, capsys):
  bot.config.SUSPICIOUS_JOIN_FREQUENCY = 1
  for i in range(8, 11):
    member = await dpytest.member_join(0, discrim=i)

  await asyncio.sleep(.1)
  assert bot._modules[0].raid_mode
  await kill_bot(bot)
