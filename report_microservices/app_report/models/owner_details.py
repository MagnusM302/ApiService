# models/owner_details.py
from pydantic import BaseModel
from typing import Optional

class OwnerDetails(BaseModel):
    name: str
    contact_information: str
    period_of_ownership: Optional[str] = None
    construction_knowledge: Optional[str] = None
