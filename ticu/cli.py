

import click

import ticu.app
import ticu.utils


app = ticu.app.App()

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
    with ticu.utils.PIDManager(pidfile, on_exists_callback=already_running):
      app.run(dev=dev)
