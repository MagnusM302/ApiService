from pydantic import BaseModel
from typing import List, Optional

class BuildingDetailsDTO(BaseModel):
    id: str
    byg007Bygningsnummer: Optional[int]
    byg021BygningensAnvendelse: str
    byg026Opførelsesår: Optional[int]
    byg032YdervæggensMateriale: str
    byg033Tagdækningsmateriale: str
    byg037KildeTilBygningensMaterialer: str
    byg038SamletBygningsareal: Optional[int]
    byg039BygningensSamledeBoligAreal: Optional[int]
    byg041BebyggetAreal: Optional[int]
    byg053BygningsarealerKilde: Optional[str]
    byg054AntalEtager: Optional[int]
    byg056Varmeinstallation: str
    byg058SupplerendeVarme: str
    byg094Revisionsdato: Optional[str]
    byg133KildeTilKoordinatsæt: Optional[str]
    byg134KvalitetAfKoordinatsæt: Optional[str]
    byg135SupplerendeOplysningOmKoordinatsæt: Optional[str]
    byg136PlaceringPåSøterritorie: Optional[str]
    byg404Koordinat: Optional[str]
    byg406Koordinatsystem: Optional[str]
    forretningshændelse: Optional[str]
    forretningsområde: Optional[str]
    forretningsproces: Optional[str]
    grund: Optional[str]
    husnummer: Optional[str]= None
    jordstykke: Optional[str]
    kommunekode: Optional[str]
    registreringFra: Optional[str]
    registreringsaktør: Optional[str]
    status: Optional[str]
    virkningFra: Optional[str]
    virkningsaktør: Optional[str]
    etageList: Optional[List] = []
    opgangList: Optional[List] = []
