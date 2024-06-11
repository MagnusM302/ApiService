# building_microservices/app_building/dtos/building_details_dto.py
from pydantic import BaseModel
from typing import List, Optional

class BuildingDetailsDTO(BaseModel):
    id_lokalId: str
    byg007Bygningsnummer: int
    byg021BygningensAnvendelse: str
    byg026Opførelsesår: int
    byg032YdervæggensMateriale: str
    byg033Tagdækningsmateriale: str
    byg037KildeTilBygningensMaterialer: str
    byg038SamletBygningsareal: int
    byg039BygningensSamledeBoligAreal: int
    byg041BebyggetAreal: int
    byg053BygningsarealerKilde: str
    byg054AntalEtager: int
    byg056Varmeinstallation: str
    byg058SupplerendeVarme: str
    byg094Revisionsdato: str
    byg133KildeTilKoordinatsæt: str
    byg134KvalitetAfKoordinatsæt: str
    byg135SupplerendeOplysningOmKoordinatsæt: str
    byg136PlaceringPåSøterritorie: str
    byg404Koordinat: str
    byg406Koordinatsystem: str
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