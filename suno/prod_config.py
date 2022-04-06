
MAIN_SERVER:int = 987654321
SERVERS:tuple = (MAIN_SERVER, )


### Those are just constantes to use in the code.
### Their value should not be important.
ROLE_CONFIANCE_HAUTE:str = "1"
ROLE_CONFIANCE_MOYENNE:str = "2"
ROLE_CONFIANCE_BASSE:str = "3"

ROLE_NAME_TO_CODE = {
  ### roles names for __this specific__ server
  MAIN_SERVER: {
    "role_confiance_haute": ROLE_CONFIANCE_HAUTE,
    "role_confiance_moyenne": ROLE_CONFIANCE_MOYENNE,
    "role_confiance_basse": ROLE_CONFIANCE_BASSE,
  }
}