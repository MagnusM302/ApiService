from pydantic import BaseModel
from typing import List, Optional
from .building_details_dto import BuildingDetailsDTO

class HouseDetailsDTO(BaseModel):
    id: str
    address: str
    year_built: int
    total_area: int
    number_of_buildings: int
    main_building_details: BuildingDetailsDTO
    additional_buildings: List[BuildingDetailsDTO] = []
    owner_details: dict
    hustype: dict
