# models/damage_details.py
from pydantic import BaseModel
from shared.enums import DamageSeverity

class DamageDetails(BaseModel):
    description: str
    severity: DamageSeverity
    location: str
