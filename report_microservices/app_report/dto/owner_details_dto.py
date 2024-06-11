# owner_details_dto.py
from pydantic import BaseModel
from typing import Optional

class OwnerDetailsDTO(BaseModel):
    name: str
    contact_information: str
    period_of_ownership: Optional[str] = None
    construction_knowledge: Optional[str] = None
