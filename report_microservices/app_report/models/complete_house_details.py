# models/complete_house_details.py
from pydantic import BaseModel
from typing import Optional
from .report_building_details import ReportBuildingDetails
from .owner_details import OwnerDetails

class CompleteHouseDetails(ReportBuildingDetails):
    seller_info: OwnerDetails