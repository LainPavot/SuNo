


SQLITE_PATH = "ticu.sqlite"
SUSPICIOUS_JOIN_FREQUENCY = 1

DEBUG_DATABASE = False

LOAD_COMMAND = "!app load"


TEST = True

if TEST:
  from ticu.test_config import *

else:
  from ticu.prod_config import *


ROLE_CODE_TO_NAME = {
  server: {
    value: key
    for key, value in ROLE_NAME_TO_CODE[server].items()
  } for server in ROLE_NAME_TO_CODE
}

ROLES = {}

