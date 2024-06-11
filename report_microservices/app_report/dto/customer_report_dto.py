from pydantic import BaseModel
from typing import Optional

class CustomerReportDTO(BaseModel):
    id: Optional[str] = None  # ID genereres af databasen
    name: str
    phone: str  # Telefonnummer
    email: str
    address: str

    # Felter fra tilstandsrapporten
    bestilling_oplysninger: Optional[str] = None  # Hvordan fandt du den bygningssagkyndige?
    ejendomsmægler: Optional[str] = None  # Har du en ejendomsmægler?
    ejer_år: Optional[int] = None  # Hvor mange år har du ejet ejendommen?
    boet_periode: Optional[str] = None  # I hvilken periode har du boet på ejendommen?
    tilbygninger: Optional[str] = None  # Har du kendskab til, at der er udført tilbygninger?
    ombygninger: Optional[str] = None  # Har du kendskab til, at der er udført ombygninger?
    renoveringer: Optional[str] = None  # Har du kendskab til, at der er udført større renoveringer?
    andre_bygninger: Optional[str] = None  # Har du kendskab til, at der er opført andre bygninger?
    tag: Optional[dict] = None  # Information om taget
    ydermur: Optional[dict] = None  # Information om ydermur
    indre_vægge: Optional[dict] = None  # Information om indre vægge
    fundamenter: Optional[dict] = None  # Information om fundamenter
    kælder: Optional[dict] = None  # Information om kælder
    gulve: Optional[dict] = None  # Information om gulve
    vinduer_døre: Optional[dict] = None  # Information om vinduer og døre
    lofter_etageadskillelser: Optional[dict] = None  # Information om lofter og etageadskillelser
    vådrum: Optional[dict] = None  # Information om vådrum
    vvs: Optional[dict] = None  # Information om VVS
