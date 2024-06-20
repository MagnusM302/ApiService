# inspector_report_dto.py

from pydantic import BaseModel, Field
from typing import Optional, List
from .complete_house_details_dto import CompleteHouseDetailsDTO
from .building_component_dto import BuildingComponentDTO

class InspectorReportDTO(BaseModel):
    id: Optional[str] = None
    customer_report_id: str
    fetched_complete_house_details: CompleteHouseDetailsDTO
    discrepancies: Optional[str] = Field(default="", description="List of discrepancies found")
    inspector_comments: Optional[str] = Field(default="", description="Comments from the inspector")
    inspection_date: Optional[str] = Field(default="", description="Date of the inspection")
    inspector_name: Optional[str] = Field(default="", description="Name of the inspector")
    inspector_signature: Optional[str] = Field(default="", description="Signature of the inspector")
    building_components: List[BuildingComponentDTO] = Field(default_factory=list, description="List of building components")