
import pytest
import asyncio

import ticu.app
import ticu.config
import ticu.modules

import discord
import discord.flags
import discord.ext.test as dpytest


from .utils import bot


@pytest.mark.asyncio
async def test_welcome_one(bot, capsys):
  member = await dpytest.member_join(0, discrim=1)
  await asyncio.sleep(.1)
  guild = dpytest.runner._cur_config.guilds[0]
  await asyncio.sleep(.1)
  assert dpytest.verify().message().contains().content(
    f"Welcome {member.mention} to {guild.name}!"
  )

@pytest.mark.asyncio
async def test_welcome_three(bot, capsys):
  bot.config.SUSPICIOUS_JOIN_FREQUENCY = 0.1
  for i in range(2, 5):
    member = await dpytest.member_join(0, discrim=i)
    guild = dpytest.runner._cur_config.guilds[0]
    await asyncio.sleep(bot.config.SUSPICIOUS_JOIN_FREQUENCY)
    assert dpytest.verify().message().contains().content(
      f"Welcome {member.mention} to {guild.name}!"
    )
  await asyncio.sleep(.1)
