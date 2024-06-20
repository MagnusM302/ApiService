from pydantic import BaseModel
from typing import Optional, Dict

class CustomerReportDTO(BaseModel):
    id: Optional[str] = None
    name: str
    phone: str
    email: str
    address: str
    bestilling_oplysninger: Optional[str] = None
    ejendomsmægler: Optional[str] = None
    ejer_år: Optional[str] = None
    boet_periode: Optional[str] = None
    tilbygninger: Optional[str] = None
    ombygninger: Optional[str] = None
    renoveringer: Optional[str] = None
    andre_bygninger: Optional[str] = None
    tag: Optional[str] = None  # Changed to string
    ydermur: Optional[str] = None  # Changed to string
    indre_vægge: Optional[str] = None  # Changed to string
    fundamenter: Optional[str] = None  # Changed to string
    kælder: Optional[str] = None  # Changed to string
    gulve: Optional[str] = None  # Changed to string
    vinduer_døre: Optional[str] = None  # Changed to string
    lofter_etageadskillelser: Optional[str] = None  # Changed to string
    vådrum: Optional[str] = None  # Changed to string
    vvs: Optional[str] = None  # Changed to string
