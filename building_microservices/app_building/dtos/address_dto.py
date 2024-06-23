# building_microservices/app_building/dtos/address_dto.py
from pydantic import BaseModel
from typing import Optional

class AddressDTO(BaseModel):
    id: str
    status: Optional[int]
    darstatus: Optional[int]
    vejkode: Optional[str]
    vejnavn: str
    adresseringsvejnavn: Optional[str]
    husnr: Optional[str]
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