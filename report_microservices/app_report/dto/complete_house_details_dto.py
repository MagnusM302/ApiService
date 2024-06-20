# complete_house_details_dto.py
from pydantic import BaseModel
from typing import Optional, List
from .owner_details_dto import OwnerDetailsDTO
from .damage_details_dto import DamageDetailsDTO
from .hustype_dto import HustypeDTO
from .building_component_dto import BuildingComponentDTO
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme

class CompleteHouseDetailsDTO(BaseModel):
    id: str
    address: str
    year_built: str
    total_area: float
    number_of_buildings: int
    owner_details: OwnerDetailsDTO
    hustype: HustypeDTO
    basement_present: Optional[bool] = None
    building_components: List[BuildingComponentDTO] = []
    varmeinstallation: str
    ydervaegsmateriale: str
    tagdaekningsmateriale: str
    bygningens_anvendelse: str
    kilde_til_bygningens_materialer: str
    supplerende_varme: str
    remarks: Optional[str] = None
    inspection_date: Optional[str] = None
    inspector_name: Optional[str] = None
    inspector_signature: Optional[str] = None
