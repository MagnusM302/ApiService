# complete_house_details_dto.py
from pydantic import BaseModel
from typing import Optional, List
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme

class CompleteHouseDetailsDTO(BaseModel):
    id: str
    address: str
    year_built: str
    total_area: float
    number_of_buildings: int
    basement_present: Optional[bool] = None
    varmeinstallation: str
    ydervaegsmateriale: str
    tagdaekningsmateriale: str
    bygningens_anvendelse: str
    kilde_til_bygningens_materialer: str
    supplerende_varme: str
    
