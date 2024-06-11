# building_microservices/app_building/models/building_details.py
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from shared.enums import (
    Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale,
    BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
)

class BuildingDetails(BaseModel):
    id: str
    byg007Bygningsnummer: Optional[int] = None
    byg021BygningensAnvendelse: BygningensAnvendelse
    byg026Opførelsesår: Optional[int] = None
    byg032YdervæggensMateriale: YdervæggensMateriale
    byg033Tagdækningsmateriale: TagdækningsMateriale
    byg037KildeTilBygningensMaterialer: KildeTilBygningensMaterialer
    byg038SamletBygningsareal: Optional[int] = None
    byg039BygningensSamledeBoligAreal: Optional[int] = None
    byg041BebyggetAreal: Optional[int] = None
    byg053BygningsarealerKilde: Optional[str] = None
    byg054AntalEtager: Optional[int] = None
    byg056Varmeinstallation: Varmeinstallation
    byg058SupplerendeVarme: SupplerendeVarme
    byg094Revisionsdato: Optional[str] = None
    byg133KildeTilKoordinatsæt: Optional[str] = None
    byg134KvalitetAfKoordinatsæt: Optional[str] = None
    byg135SupplerendeOplysningOmKoordinatsæt: Optional[str] = None
    byg136PlaceringPåSøterritorie: Optional[str] = None
    byg404Koordinat: Optional[str] = None
    byg406Koordinatsystem: Optional[str] = None
    forretningshændelse: Optional[str] = None
    forretningsområde: Optional[str] = None
    forretningsproces: Optional[str] = None
    grund: Optional[str] = None
    husnummer: Optional[str] = None
    jordstykke: Optional[str] = None
    kommunekode: Optional[str] = None
    registreringFra: Optional[str] = None
    registreringsaktør: Optional[str] = None
    status: Optional[str] = None
    virkningFra: Optional[str] = None
    virkningsaktør: Optional[str] = None
    etageList: Optional[List] = []
    opgangList: Optional[List] = []

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.convert_enums(data)

    @classmethod
    def from_dict(cls, data):
        data = cls.reconstruct_enums(data)
        return cls(**data)

    @staticmethod
    def convert_enums(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, Enum):
                    d[k] = v.value
                elif isinstance(v, list):
                    d[k] = [BuildingDetails.convert_enums(item) for item in v]
                elif isinstance(v, dict):
                    d[k] = BuildingDetails.convert_enums(v)
        elif isinstance(d, list):
            d = [BuildingDetails.convert_enums(item) for item in d]
        return d

    @staticmethod
    def reconstruct_enums(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in Varmeinstallation.__members__:
                    d[k] = Varmeinstallation(v)
                elif k in YdervæggensMateriale.__members__:
                    d[k] = YdervæggensMateriale(v)
                elif k in TagdækningsMateriale.__members__:
                    d[k] = TagdækningsMateriale(v)
                elif k in BygningensAnvendelse.__members__:
                    d[k] = BygningensAnvendelse(v)
                elif k in KildeTilBygningensMaterialer.__members__:
                    d[k] = KildeTilBygningensMaterialer(v)
                elif k in SupplerendeVarme.__members__:
                    d[k] = SupplerendeVarme(v)
                elif isinstance(v, list):
                    d[k] = [BuildingDetails.reconstruct_enums(item) for item in v]
                elif isinstance(v, dict):
                    d[k] = BuildingDetails.reconstruct_enums(v)
        elif isinstance(d, list):
            d = [BuildingDetails.reconstruct_enums(item) for item in d]
        return d
