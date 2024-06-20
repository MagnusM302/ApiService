
from .complete_house_details import CompleteHouseDetails
from .building_component import BuildingComponent

from pydantic import BaseModel, Field
from typing import Optional, List

class InspectorReport(BaseModel):
    id: Optional[str] = None
    customer_report_id: str
    fetched_building_details: CompleteHouseDetails  
    discrepancies: Optional[str] = ""
    inspector_comments: Optional[str] = ""
    inspection_date: Optional[str] = ""
    inspector_name: Optional[str] = ""
    inspector_signature: Optional[str] = ""
    building_components: List[BuildingComponent] = []
