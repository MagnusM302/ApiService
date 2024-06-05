from enum import Enum

class BygningensAnvendelse(Enum):
    STUEHUS_TIL_LANDBRUGSEJENDOM = "110"
    FRITLIGGENDE_ENFAMILIEHUS = "120"
    SAMMENBYGGET_ENFAMILIEHUS = "121"
    FRITLIGGENDE_ENFAMILIEHUS_I_TÆT_LAV_BEBYGGELSE = "122"
    RÆKKE_KÆDE_ELLER_DOBBELTHUS_UDFASES = "130"
    RÆKKE_KÆDE_OG_KLYNGEHUS = "131"
    DOBBELTHUS = "132"
    ETAGEBOLIG_BYGNING_FLERFAMILIEHUS_ELLER_TO_FAMILIEHUS = "140"
    KOLLEGIUM = "150"
    BOLIGBYGNING_TIL_DØGNINSTITUTION = "160"
    ANNEKS_I_TILKNYTNING_TIL_HELÅRSBOLIG = "185"
    ANDEN_BYGNING_TIL_HELÅRSBEOELSE = "190"
    BYGNING_TIL_ERHVERVSMÆSSIG_PRODUKTION_VEDRØRENDE_LANDBRUG_GARTNERI_RÅSTOFUDVINDING_O_LIGN_UDFASES = "210"
    STALD_TIL_SVIN = "211"
    STALD_TIL_KVÆG_FÅR_MV = "212"
    STALD_TIL_FJERKRÆ = "213"
    MINKHAL = "214"
    VÆKSTHUS = "215"
    LADE_TIL_FODER_AFGRØDER_MV = "216"
    MASKINHUS_GARAGE_MV = "217"
    LADE_TIL_HALM_HØ_MV = "218"
    ANDEN_BYGNING_TIL_LANDBRUG_MV = "219"
    BYGNING_TIL_ERHVERVSMÆSSIG_PRODUKTION_VEDRØRENDE_INDUSTRI_HÅNDVÆRK_MV_FABRIK_VÆRKSTED_O_LIGN_UDFASES = "220"
    BYGNING_TIL_INDUSTRI_MED_INTEGRERET_PRODUKTIONSAPPARAT = "221"
    BYGNING_TIL_INDUSTRI_UDEN_INTEGRERET_PRODUKTIONSAPPARAT = "222"
    VÆRKSTED = "223"
    ANDEN_BYGNING_TIL_PRODUKTION = "229"
    BYGNING_TIL_EL_GAS_VAND_ELLER_VARMEVÆRK_FORBRÆNDINGSANSTALT_MV_UDFASES = "230"
    BYGNING_TIL_ENERGIPRODUKTION = "231"
    BYGNING_TIL_ENERGIDISTRIBUTION = "232"
    BYGNING_TIL_VANDFORSYNING = "233"
    BYGNING_TIL_HÅNDTERING_AF_AFFALD_OG_SPILDEVAND = "234"
    ANDEN_BYGNING_TIL_ENERGIPRODUKTION_OG_FORSYNING = "239"
    ANDEN_BYGNING_TIL_LANDBRUG_INDUSTRI_ETC_UDFASES = "290"
    TRANSPORT_OG_GARAGEANLÆG_UDFASES = "310"
    BYGNING_TIL_JERNBANE_OG_BUSDRIFT = "311"
    BYGNING_TIL_LUFTFART = "312"
    BYGNING_TIL_PARKERING_OG_TRANSPORTANLÆG = "313"
    BYGNING_TIL_PARKERING_AF_FLERE_END_TO_KØRETØJER_I_TILKNYTNING_TIL_BOLIGER = "314"
    HAVNEANLÆG = "315"
    ANDET_TRANSPORTANLÆG = "319"
    BYGNING_TIL_KONTOR_HANDEL_LAGER_HERUNDER_OFFENTLIG_ADMINISTRATION_UDFASES = "320"
    BYGNING_TIL_KONTOR = "321"
    BYGNING_TIL_DETAILHANDEL = "322"
    BYGNING_TIL_LAGER = "323"
    BUTIKSCENTER = "324"
    TANKSTATION = "325"
    ANDEN_BYGNING_TIL_KONTOR_HANDEL_OG_LAGER = "329"
    BYGNING_TIL_HOTEL_RESTAURANT_VASKERI_FRISØR_OG_ANDEN_SERVICEVIRKSOMHED_UDFASES = "330"
    HOTEL_KRO_ELLER_KONFERENCECENTER_MED_OVERNATNING = "331"
    BED_AND_BREAKFAST_MV = "332"
    RESTAURANT_CAFÉ_OG_KONFERENCECENTER_UDEN_OVERNATNING = "333"
    PRIVAT_SERVICEVIRKSOMHED_SOM_FRISØR_VASKERI_NETCAFÉ_MV = "334"
    ANDEN_BYGNING_TIL_SERVICEERHVERV = "339"
    ANDEN_BYGNING_TIL_TRANSPORT_HANDEL_ETC_UDFASES = "390"
    BYGNING_TIL_BIOGRAF_TEATER_ERHVERVSMÆSSIG_UDSTILLING_BIBLIOTEK_MUSEUM_KIRKE_O_LIGN_UDFASES = "410"
    BIOGRAF_TEATER_KONCERTSTED_MV = "411"
    MUSEUM = "412"
    BIBLIOTEK = "413"
    KIRKE_ELLER_ANDEN_BYGNING_TIL_TROSUDØVELSE_FOR_STATSANERKENDETE_TROSSAMFUND = "414"
    FORSAMLINGSHUS = "415"
    FORLYSTELSESARK = "416"
    ANDEN_BYGNING_TIL_KULTURELLE_FORMÅL = "419"
    BYGNING_TIL_UNDERVISNING_OG_FORSKNING_UDFASES = "420"
    GRUNDSKOLE = "421"
    UNIVERSITET = "422"
    ANDEN_BYGNING_TIL_UNDERVISNING_OG_FORSKNING = "429"
    BYGNING_TIL_HOSPITAL_SYGEHJEM_FØDEKLINIK_O_LIGN_UDFASES = "430"
    HOSPITAL_OG_SYGEHUS = "431"
    HOSPICE_BEHANDLINGSHEM_MV = "432"
    SUNDHEDSCENTER_LÆGEHUS_FØDEKLINIK_MV = "433"
    ANDEN_BYGNING_TIL_SUNDHEDSFORMÅL = "439"
    BYGNING_TIL_DAGINSTITUTION_UDFASES = "440"
    DAGINSTITUTION = "441"
    SERVICEFUNKTION_PÅ_DØGNINSTITUTION = "442"
    KASERNE = "443"
    FÆNGSEL_ARRESTHUS_MV = "444"
    ANDEN_BYGNING_TIL_INSTITUTIONSFORMÅL = "449"
    BESKYTTELSESRUM = "451"
    ANDEN_BYGNING_TIL_ANDEN_INSTITUTION_HERUNDER_KASERNE_FÆNGSEL_O_LIGN_UDFASES = "490"
    SOMMERHUS = "510"
    BYGNING_TIL_FERIEKOLONI_VANDREHJEM_O_LIGN_BORTSET_FRA_SOMMERHUS_UDFASES = "520"
    FERIECENTER_CENTER_TIL_CAMPINGPLADS_MV = "521"
    BYGNING_MED_FERIELEJLIGHEDER_TIL_ERHVERVSMÆSSIG_UDLEJNING = "522"
    BYGNING_MED_FERIELEJLIGHEDER_TIL_EGET_BRUG = "523"
    ANDEN_BYGNING_TIL_FERIEFORMÅL = "529"
    BYGNING_I_FORBINDELSE_MED_IDRÆTSUDØVELSE_KLUBHUS_IDRÆTSHAL_SVØMMEHAL_O_LIGN_UDFASES = "530"
    KLUBHUS_I_FORBINDELSE_MED_FRITID_OG_IDRÆT = "531"
    SVØMMEHAL = "532"
    IDRÆTSHAL = "533"
    TRIBUNE_I_FORBINDELSE_MED_STADION = "534"
    BYGNING_TIL_TRÆNING_OG_OPSTALDNING_AF_HESTE = "535"
    ANDEN_BYGNING_TIL_IDRÆTSFORMÅL = "539"
    KOLONIHAVEHUS = "540"
    ANNEKS_I_TILKNYTNING_TIL_FRITIDS_OG_SOMMERHUS = "585"
    ANDEN_BYGNING_TIL_FRITIDSFORMÅL = "590"
    GARAGE = "910"
    CARPORT = "920"
    UDHUS = "930"
    DRIVHUS = "940"
    FRITLIGGENDE_OVERDÆKNING = "950"
    FRITLIGGENDE_UDESTUE = "960"
    TILOVERSBLEVEN_LANDBRUGSBYGNING = "970"
    FALDEFÆRDIG_BYGNING = "990"
    UKENDT_BYGNING = "999"

    def __str__(self):
        enum_strings = {
            "110": "Stuehus til landbrugsejendom",
            "120": "Fritliggende enfamiliehus",
            "121": "Sammenbygget enfamiliehus",
            "122": "Fritliggende enfamiliehus i tæt-lav bebyggelse",
            "130": "(UDFASES) Række-, kæde-, eller dobbelthus (lodret adskillelse mellem enhederne).",
            "131": "Række-, kæde- og klyngehus",
            "132": "Dobbelthus",
            "140": "Etagebolig-bygning, flerfamiliehus eller to-familiehus",
            "150": "Kollegium",
            "160": "Boligbygning til døgninstitution",
            "185": "Anneks i tilknytning til helårsbolig",
            "190": "Anden bygning til helårsbeboelse",
            "210": "(UDFASES) Bygning til erhvervsmæssig produktion vedrørende landbrug, gartneri, råstofudvinding o. lign",
            "211": "Stald til svin",
            "212": "Stald til kvæg, får mv.",
            "213": "Stald til fjerkræ",
            "214": "Minkhal",
            "215": "Væksthus",
            "216": "Lade til foder, afgrøder mv.",
            "217": "Maskinhus, garage mv.",
            "218": "Lade til halm, hø mv.",
            "219": "Anden bygning til landbrug mv.",
            "220": "(UDFASES) Bygning til erhvervsmæssig produktion vedrørende industri, håndværk m.v. (fabrik, værksted o.lign.)",
            "221": "Bygning til industri med integreret produktionsapparat",
            "222": "Bygning til industri uden integreret produktionsapparat",
            "223": "Værksted",
            "229": "Anden bygning til produktion",
            "230": "(UDFASES) El-, gas-, vand- eller varmeværk, forbrændingsanstalt m.v.",
            "231": "Bygning til energiproduktion",
            "232": "Bygning til energidistribution",
            "233": "Bygning til vandforsyning",
            "234": "Bygning til håndtering af affald og spildevand",
            "239": "Anden bygning til energiproduktion og forsyning",
            "290": "(UDFASES) Anden bygning til landbrug, industri etc.",
            "310": "(UDFASES) Transport- og garageanlæg (fragtmandshal, lufthavnsbygning, banegårdsbygning, parkeringshus). Garage med plads til et eller to køretøjer registreres med anvendelseskode 910",
            "311": "Bygning til jernbane- og busdrift",
            "312": "Bygning til luftfart",
            "313": "Bygning til parkering- og transportanlæg",
            "314": "Bygning til parkering af flere end to køretøjer i tilknytning til boliger",
            "315": "Havneanlæg",
            "319": "Andet transportanlæg",
            "320": "(UDFASES) Bygning til kontor, handel, lager, herunder offentlig administration",
            "321": "Bygning til kontor",
            "322": "Bygning til detailhandel",
            "323": "Bygning til lager",
            "324": "Butikscenter",
            "325": "Tankstation",
            "329": "Anden bygning til kontor, handel og lager",
            "330": "(UDFASES) Bygning til hotel, restaurant, vaskeri, frisør og anden servicevirksomhed",
            "331": "Hotel, kro eller konferencecenter med overnatning",
            "332": "Bed & breakfast mv.",
            "333": "Restaurant, café og konferencecenter uden overnatning",
            "334": "Privat servicevirksomhed som frisør, vaskeri, netcafé mv.",
            "339": "Anden bygning til serviceerhverv",
            "390": "(UDFASES) Anden bygning til transport, handel etc",
            "410": "(UDFASES) Bygning til biograf, teater, erhvervsmæssig udstilling, bibliotek, museum, kirke o. lign.",
            "411": "Biograf, teater, koncertsted mv.",
            "412": "Museum",
            "413": "Bibliotek",
            "414": "Kirke eller anden bygning til trosudøvelse for statsanerkendte trossamfund",
            "415": "Forsamlingshus",
            "416": "Forlystelsespark",
            "419": "Anden bygning til kulturelle formål",
            "420": "(UDFASES) Bygning til undervisning og forskning (skole, gymnasium, forskningslabratorium o.lign.).",
            "421": "Grundskole",
            "422": "Universitet",
            "429": "Anden bygning til undervisning og forskning",
            "430": "(UDFASES) Bygning til hospital, sygehjem, fødeklinik o. lign.",
            "431": "Hospital og sygehus",
            "432": "Hospice, behandlingshjem mv.",
            "433": "Sundhedscenter, lægehus, fødeklinik mv.",
            "439": "Anden bygning til sundhedsformål",
            "440": "(UDFASES) Bygning til daginstitution",
            "441": "Daginstitution",
            "442": "Servicefunktion på døgninstitution",
            "443": "Kaserne",
            "444": "Fængsel, arresthus mv.",
            "449": "Anden bygning til institutionsformål",
            "451": "Beskyttelsesrum",
            "490": "(UDFASES) Bygning til anden institution, herunder kaserne, fængsel o. lign.",
            "510": "Sommerhus",
            "520": "(UDFASES) Bygning til feriekoloni, vandrehjem o.lign. bortset fra sommerhus",
            "521": "Feriecenter, center til campingplads mv.",
            "522": "Bygning med ferielejligheder til erhvervsmæssig udlejning",
            "523": "Bygning med ferielejligheder til eget brug",
            "529": "Anden bygning til ferieformål",
            "530": "(UDFASES) Bygning i forbindelse med idrætsudøvelse (klubhus, idrætshal, svømmehal o. lign.)",
            "531": "Klubhus i forbindelse med fritid og idræt",
            "532": "Svømmehal",
            "533": "Idrætshal",
            "534": "Tribune i forbindelse med stadion",
            "535": "Bygning til træning og opstaldning af heste",
            "539": "Anden bygning til idrætformål",
            "540": "Kolonihavehus",
            "585": "Anneks i tilknytning til fritids- og sommerhus",
            "590": "Anden bygning til fritidsformål",
            "910": "Garage",
            "920": "Carport",
            "930": "Udhus",
            "940": "Drivhus",
            "950": "Fritliggende overdækning",
            "960": "Fritliggende udestue",
            "970": "Tiloversbleven landbrugsbygning",
            "990": "Faldefærdig bygning",
            "999": "Ukendt bygning"
        }
        return enum_strings[self.value]

