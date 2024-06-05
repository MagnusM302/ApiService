from enum import Enum

class YdervaeggensMateriale(Enum):
    Mursten = "1"
    LETBETONSTEN = "2"
    FIBERCEMENT_HERUNDER_ASBEST = "3"
    BINDINGSVÆRK = "4"
    TRÆ = "5"
    BETONELEMENTER = "6"
    METAL = "8"
    FIBERCEMENT_UDEN_ASBEST = "10"
    PLASTMATERIALER = "11"
    GLAS = "12"
    INGEN = "80"
    ANDET_MATERIALE = "90"

    def __str__(self):
        enum_strings = {
            "1": "Mursten",
            "2": "Træ",
            "3": "Fibercement (herunder asbest)",
            "4": "Bindingsværk",
            "5": "Tegl",
            "6": "Betonelementer",
            "8": "Metal",
            "10": "Fibercement (uden asbest)",
            "11": "Plastmaterialer",
            "12": "Glas",
            "80": "Ingen",
            "90": "Annet materiale"
        }
        return enum_strings[self.value]

class TagdaekningsMateriale(Enum):
    TAGPAP_MED_LILLE_HAELDNING = "1"
    TAGPAP_MED_STOR_HAELDNING = "2"
    FIBERCEMENT_HERUNDER_ASBEST = "3"
    BETONTAGSTEN = "4"
    TEGL = "5"
    METAL = "6"
    STRAATAG = "7"
    FIBERCEMENT_UDEN_ASBEST = "10"
    PLASTMATERIALER = "11"
    GLAS = "12"
    LEVENDE_TAGE = "20"
    UDFASES_INGEN = "80"
    ANDET_MATERIALE = "90"

    def __str__(self):
        enum_strings = {
            "1": "Tagpap med lille hældning",
            "2": "Tagpap med stor hældning",
            "3": "Fibercement herunder asbest",
            "4": "Betontagsten",
            "5": "Tegl",
            "6": "Metal",
            "7": "Stråtag",
            "10": "Fibercement uden asbest",
            "11": "Plastmaterialer",
            "12": "Glas",
            "20": "Levende tage",
            "80": "(UDFASES) Ingen",
            "90": "Andet materiale"
        }
        return enum_strings[self.value]