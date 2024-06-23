from pydantic import BaseModel

class Address(BaseModel):
    vejnavn: str
    husnr: str
    postnr: str
    postnrnavn: str
    tekst: str
    adgangsadresseid: str
