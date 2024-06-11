# models/address.py

from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    id: str
    status: Optional[int]
    darstatus: Optional[int]
    vejkode: Optional[str]
    vejnavn: str
    adresseringsvejnavn: Optional[str]
    husnr: str
    etage: Optional[str] = None
    dør: Optional[str] = None
    supplerendebynavn: Optional[str] = None
    postnr: str
    postnrnavn: str
    stormodtagerpostnr: Optional[bool] = False
    stormodtagerpostnrnavn: Optional[str] = None
    kommunekode: Optional[str]
    adgangsadresseid: str
    x: Optional[float]
    y: Optional[float]
    href: Optional[str]
    tekst: Optional[str] = ""

    class Config:
        arbitrary_types_allowed = True