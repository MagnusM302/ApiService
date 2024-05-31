# building_microservices/app_building/models/address.py
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    id: str
    status: int
    darstatus: int
    vejkode: str
    vejnavn: str
    adresseringsvejnavn: str
    husnr: str
    etage: Optional[str] = None
    dør: Optional[str] = None
    supplerendebynavn: Optional[str] = None
    postnr: str
    postnrnavn: str
    stormodtagerpostnr: bool
    stormodtagerpostnrnavn: Optional[str] = None
    kommunekode: str
    adgangsadresseid: str
    x: float
    y: float
    href: str
    tekst: Optional[str] = None
