# models/complete_house_details.py
from pydantic import BaseModel
from typing import Optional, List
from .owner_details import OwnerDetails
from .damage_details import DamageDetails
from .hustype import Hustype
from .building_component import BuildingComponent
from shared.enums import DamageSeverity, Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme

class CompleteHouseDetails(BaseModel):
    id: str
    address: str
    year_built: str
    total_area: float
    number_of_buildings: int
    owner_details: OwnerDetails
    hustype: Hustype
    basement_present: Optional[bool] = None
    building_components: List[BuildingComponent] = []
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