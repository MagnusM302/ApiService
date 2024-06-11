#building_component_dto.py
from pydantic import BaseModel
from typing import Optional
from .damage_details_dto import DamageDetailsDTO

class BuildingComponentDTO(BaseModel):
    name: str
    condition: str
    damage: Optional[DamageDetailsDTO] = None
    remarks: Optional[str] = None