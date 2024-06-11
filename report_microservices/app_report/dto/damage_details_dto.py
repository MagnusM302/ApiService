# damage_details_dto.py
from pydantic import BaseModel
from shared.enums import DamageSeverity

class DamageDetailsDTO(BaseModel):
    description: str
    severity: DamageSeverity
    location: str
