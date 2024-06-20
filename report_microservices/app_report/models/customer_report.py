from pydantic import BaseModel
from typing import Optional

class CustomerReport(BaseModel):
    id: Optional[str] = None
    name: str
    phone: str
    email: str
    address: str
    bestilling_oplysninger: str
    ejendomsmægler: str
    ejer_år: str  # Changed to str
    boet_periode: str
    tilbygninger: str
    ombygninger: str
    renoveringer: str
    andre_bygninger: str
    tag: str  # Changed to str
    ydermur: str  # Changed to str
    indre_vægge: str  # Changed to str
    fundamenter: str  # Changed to str
    kælder: str  # Changed to str
    gulve: str  # Changed to str
    vinduer_døre: str  # Changed to str
    lofter_etageadskillelser: str  # Changed to str
    vådrum: str  # Changed to str
    vvs: str  # Changed to str
