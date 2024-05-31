from pydantic import BaseModel
from typing import List
from .damage_details import DamageDetails
from .building_common_details import BuildingCommonDetails

class BuildingDetails(BuildingCommonDetails):
    id: str
    year_built: int
    area: int
    rooms: int
    condition: str
    damages: List[DamageDetails] = []
