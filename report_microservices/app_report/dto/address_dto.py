from pydantic import BaseModel

class AddressDTO(BaseModel):
    vejnavn: str
    husnr: str
    postnr: str
    postnrnavn: str
    tekst: str
    adgangsadresseid: str
