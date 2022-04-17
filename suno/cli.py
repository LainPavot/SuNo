
import os


if not os.path.exists("logs"):
  os.mkdir("logs")

import click
import discord

import suno.app
import suno.utils
import suno.modules


modules = [
  suno.modules.RaidHandler,
  suno.modules.ExampleModule,
  suno.modules.NewMembers,
  suno.modules.ReactionMessage,
  suno.modules.DebugModule,
  suno.modules.ManagementModule,
]

intents = discord.Intents.all()


def build_app(token, pidfile, dev=False):
  if dev:
    app_factory = suno.app.DevApp
  else:
    app_factory = suno.app.App

  app = app_factory(intents=intents)

  app.token = token
  app.pidfile = pidfile

  for module in modules:
    module = module(app)
    app.register(module)

  return app


def already_running(pid):
  raise RuntimeError(f"This bot is already running - pid: {pid}.")


token_option = lambda:click.option(
  "--token",
  prompt="Discord token",
  help="Provide the discord token"
)
pid_option = lambda:click.option(
  "--pidfile",
  prompt="PID file path",
  help="Provide the pid file path"
)

@click.group()
def cli():
  pass

@cli.command(help="Starts the bot")
@token_option()
@pid_option()
@click.option(
  "--dev",
  is_flag=True,
  default=False,
  help="Use the dev server of the tipoui community"
)
def run(token, pidfile, dev=False):
  if dev:
    return _run_dev(token, pidfile)
  app = build_app(token, pidfile, dev=dev)
  app.run()

@cli.command(help="Starts the bot in dev mode")
@token_option()
@pid_option()
def run_dev(token, pidfile):
  return _run_dev(token, pidfile)

def _run_dev(token, pidfile):
  app = build_app(token, pidfile, dev=True)
  with suno.utils.PIDManager(
    pidfile,
    on_exists_callback=already_running
  ):
    app.run(dev=True)