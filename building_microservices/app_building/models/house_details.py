from pydantic import BaseModel
from typing import List, Optional
from .building_details import BuildingDetails
from .owner_details import OwnerDetails
from .hustype import Hustype
from .building_common_details import BuildingCommonDetails

class HouseDetails(BuildingCommonDetails):
    id: str
    address: str
    year_built: int
    total_area: int
    number_of_buildings: int
    main_building_details: BuildingDetails
    additional_buildings: List[BuildingDetails] = []
    owner_details: OwnerDetails
    hustype: Hustype

class CompleteHouseDetails(HouseDetails):
    seller_info: OwnerDetails