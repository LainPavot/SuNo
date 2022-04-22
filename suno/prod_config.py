
ZAD_SERVER:int = 909921769530462229
PROMENAME_SERVER:int = 779065408191594520
CONSEIL_SERVER:int = 779104471929585674
LABO_SERVER:int = 909928095908253726
SOURCES_SERVER:int = 909928095908253726
# PELUCHE_SERVER:int = 909928095908253726
SERVERS:tuple = (
  ZAD_SERVER,
  PROMENAME_SERVER,
  CONSEIL_SERVER,
  LABO_SERVER,
  SOURCES_SERVER,
  # PELUCHE_SERVER,
)

GENERIC_NAME_HAUTE_CONFIANCE = "turquoise"


### Those are just constantes to use in the code.
### Their value should not be important.
ROLE_CONFIANCE_HAUTE:str = "1"
ROLE_CONFIANCE_MOYENNE:str = "2"
ROLE_CONFIANCE_BASSE:str = "3"

ROLE_NAME_TO_CODE = {
  ### roles names for __this specific__ server
  ZAD_SERVER: {
    "💠Turquoise": ROLE_CONFIANCE_HAUTE,
    "Phosphate d'Alumine +": ROLE_CONFIANCE_MOYENNE,
    "Phosphate d'Alumine": ROLE_CONFIANCE_BASSE,
  },
  PROMENAME_SERVER: {
    "Turquoise": ROLE_CONFIANCE_HAUTE,
    "Phosplate plus": ROLE_CONFIANCE_MOYENNE,
    "Phosphate d'alumine": ROLE_CONFIANCE_BASSE,
  },
  CONSEIL_SERVER: {
    "architecte": ROLE_CONFIANCE_HAUTE,
    "inspecteurice des travaux finis": ROLE_CONFIANCE_MOYENNE,
    "": ROLE_CONFIANCE_BASSE,
  },
  LABO_SERVER: {
    "Turquoise": ROLE_CONFIANCE_HAUTE,
    "Phosplate +": ROLE_CONFIANCE_MOYENNE,
    "Phosphate d'Alumine": ROLE_CONFIANCE_BASSE,
  },
  SOURCES_SERVER: {
    "": ROLE_CONFIANCE_HAUTE,
    "": ROLE_CONFIANCE_MOYENNE,
    "": ROLE_CONFIANCE_BASSE,
  },
  # PELUCHE_SERVER: {
  #   "": ROLE_CONFIANCE_HAUTE,
  #   "": ROLE_CONFIANCE_MOYENNE,
  #   "": ROLE_CONFIANCE_BASSE,
  # },
}

# for server, roles in {
#   ZAD_SERVER: ("💠 Turquoise", "Phosphate d'Alumine +", "Phosphate d'Alumine"),
#   PROMENAME_SERVER: ("Turquoise", "Phosplate plus", "Phosphate d'alumine"),
#   CONSEIL_SERVER: ("architecte", "inspecteurice des travaux finis", ""),
#   LABO_SERVER: ("Turquoise", "Phosplate +", "Phosphate d'Alumine"),
#   SOURCES_SERVER: ("", "", ""),
#   PELUCHE_SERVER: ("", "", ""),
# }.items():
#   ROLE_NAME_TO_CODE[server] = dict(zip(
#     (ROLE_CONFIANCE_HAUTE, ROLE_CONFIANCE_MOYENNE, ROLE_CONFIANCE_BASSE)
#     roles
#   ))
