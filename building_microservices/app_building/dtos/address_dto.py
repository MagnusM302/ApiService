# building_microservices/app_building/dtos/address_dto.py
from pydantic import BaseModel
from typing import Optional

class AddressDTO(BaseModel):
    id: str
    vejkode: str
    vejnavn: str
    adresseringsvejnavn: str
    husnr: str
    postnr: str
    postnrnavn: str
    kommunekode: str
    adgangsadresseid: str
    tekst: Optional[str] = None
    x: float
    y: float
    href: str
    status: int
    darstatus: int
    stormodtagerpostnr: Optional[bool] = False

