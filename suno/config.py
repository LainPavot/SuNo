


SQLITE_PATH:str = "suno.sqlite"
SUSPICIOUS_JOIN_FREQUENCY:float = 1

DEBUG_DATABASE:bool = False

LOAD_COMMAND:str = "!app load"


TEST:bool = True

AUTO_ROLES:dict = dict()


WELCOME_MESSAGES:dict = dict()
DEFAULT_WELCOME_MESSAGE:str = "Bonjour {user.mention}, bienvenue sur {guild.name} !"


if TEST:
  from suno.test_config import *

else:
  from suno.prod_config import *


ROLE_CODE_TO_NAME:dict = {
  server: {
    value: key
    for key, value in ROLE_NAME_TO_CODE[server].items()
  } for server in ROLE_NAME_TO_CODE
}

ROLES:dict = {}

for server in ROLE_CODE_TO_NAME:
  WELCOME_MESSAGES.setdefault(server, DEFAULT_WELCOME_MESSAGE)
