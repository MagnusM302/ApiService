# building_microservices/app_building/dtos/address_dto.py
from pydantic import BaseModel

class AddressDTO(BaseModel):
    id: str
    vejkode: str
    vejnavn: str
    husnr: str
    postnr: str
    postnrnavn: str
    kommunekode: str
    tekst: str
