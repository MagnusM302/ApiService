# complete_house_details_dto.py
from pydantic import BaseModel
from typing import Optional
from .report_building_details_dto import ReportBuildingDetailsDTO
from .owner_details_dto import OwnerDetailsDTO

class CompleteHouseDetailsDTO(ReportBuildingDetailsDTO):
    seller_info: OwnerDetailsDTO