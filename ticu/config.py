


SQLITE_PATH = "ticu.sqlite"
SUSPICIOUS_JOIN_FREQUENCY = 1

DEBUG_DATABASE = False


TUTU = "TUTU"
PHO = "PHO"
PHO_PLUS = "PHO_PLUS"

ROLE_NAME_TO_CODE = {
    "nouveau rôtestle": TUTU,
    "nouveau rôtestle2": PHO,
    "nouveau rôtestle3": PHO_PLUS,
}

ROLE_CODE_TO_NAME = {
    value: key
    for key, value in ROLE_NAME_TO_CODE.items()
}

ROLES = {}

TEST = True

if TEST:
    from ticu.test_config import *