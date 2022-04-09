

import click
import discord

import suno.app
import suno.utils
import suno.modules


intents = discord.Intents.all()

app = suno.app.App(intents=intents)

modules = [
  suno.modules.RaidHandler,
  suno.modules.ExampleModule,
  suno.modules.NewMembers,
  suno.modules.ReactionMessage,
  suno.modules.DebugModule,
  suno.modules.ManagementModule,
]

for module in modules:
  module = module(app)
  app.register(module)

def already_running(pid):
  raise RuntimeError(f"This bot is already running - pid: {pid}.")

@click.group()
def cli():
  pass

@cli.command(help="Starts the bot")
@click.option("--token", prompt="Discord token", help="Provide the discord token")
@click.option("--dev", is_flag=True, default=False, help="Use the dev server of the tipoui community")
@click.option("--pidfile", help="Provide the pid file path")
def run(token, pidfile, dev=False):
  app.token = token
  app.pidfile = pidfile

  if dev:
    app.run(dev=dev)
  else:
    with suno.utils.PIDManager(pidfile, on_exists_callback=already_running):
      app.run(dev=dev)
