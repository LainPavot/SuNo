

MAIN_SERVER:int = 915547901378322443
PLATIPUS_SERVER:int = 959888328927375430
SERVERS:tuple = (
  MAIN_SERVER,
  PLATIPUS_SERVER,
)

AUTO_ROLES = {
  MAIN_SERVER: ("sdl", 962400828801572964),
  PLATIPUS_SERVER: ("platipus", 962418121589792889),
}

OVERWRITES_ROLES:bool = True

GENERIC_NAME_HAUTE_CONFIANCE = "platipus"

### Those are just constantes to use in the code.
### Their value should not be important.
ROLE_CONFIANCE_HAUTE:str = "1"
ROLE_CONFIANCE_MOYENNE:str = "2"
ROLE_CONFIANCE_BASSE:str = "3"

ROLE_NAME_TO_CODE:dict = {
  ### roles names for __this specific__ server
  MAIN_SERVER: {
    "role_confiance_haute": ROLE_CONFIANCE_HAUTE,
    "role_confiance_moyenne": ROLE_CONFIANCE_MOYENNE,
    "role_confiance_basse": ROLE_CONFIANCE_BASSE,
  },
  PLATIPUS_SERVER: {
    "platipus joyeu·se·x": ROLE_CONFIANCE_BASSE,
    "platipus heureu·se·x": ROLE_CONFIANCE_MOYENNE,
    "platipus euphorique": ROLE_CONFIANCE_HAUTE,
  }
}

