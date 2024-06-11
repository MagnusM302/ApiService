#building_component.py
from pydantic import BaseModel
from typing import Optional
from .damage_details import DamageDetails

class BuildingComponent(BaseModel):
    name: str
    condition: str
    damage: Optional[DamageDetails] = None
    remarks: Optional[str] = None