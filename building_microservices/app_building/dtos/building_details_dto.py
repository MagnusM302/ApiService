from pydantic import BaseModel
from typing import Optional

class BuildingDetailsDTO(BaseModel):
    id: str
    year_built: int
    area: int
    rooms: int
    condition: str
    wall_conditions: Optional[str] = None
    roof_conditions: Optional[str] = None
    floor_conditions: Optional[str] = None
    windows_doors_conditions: Optional[str] = None
    moisture_mold: Optional[str] = None
    electrical_system: Optional[str] = None
    plumbing_system: Optional[str] = None
    heating_system: Optional[str] = None
    asbestos: Optional[str] = None
    radon: Optional[str] = None
    lead_paint: Optional[str] = None
    exterior_walls: Optional[str] = None
    yard_landscaping: Optional[str] = None
    driveways_walkways: Optional[str] = None
    interior_rooms: Optional[str] = None
    attic_conditions: Optional[str] = None
    basement_conditions: Optional[str] = None
    insulation: Optional[str] = None
