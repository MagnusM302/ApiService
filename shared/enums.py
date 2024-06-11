# shared/enums.py

from enum import Enum

class Varmeinstallation(Enum):
    NONE = "0"
    CENTRAL = "1"
    FJERNVARME = "2"
    GAS = "3"
    EL = "4"
    OTHER = "5"
    JORDVARME = "6"

class YdervæggensMateriale(Enum):
    BRICK = "1"
    CONCRETE = "2"
    WOOD = "3"
    STEEL = "4"
    OTHER = "5"

class TagdækningsMateriale(Enum):
    TILE = "1"
    SLATE = "2"
    METAL = "3"
    OTHER = "4"

class BygningensAnvendelse(Enum):
    RESIDENTIAL = "120"
    COMMERCIAL = "130"
    INDUSTRIAL = "140"
    AGRICULTURAL = "150"
    OTHER = "160"

class KildeTilBygningensMaterialer(Enum):
    LOCAL = "Local"
    IMPORTED = "Imported"
    INTERNAL = "1"
    EXTERNAL = "2"


class SupplerendeVarme(Enum):
    NONE = "0"
    WOOD = "1"
    OIL = "2"
    GAS = "3"
    ELECTRIC = "4"
    OTHER = "5"


class DamageSeverity(Enum):
    CRITICAL = ("Critical", "Red")
    MAJOR = ("Major", "Orange")
    MINOR = ("Minor", "Yellow")
    NONE = ("None", "Green")




