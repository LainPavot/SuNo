

import click

import ticu.app


app = ticu.app.App()

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
  app.run(dev=dev)
