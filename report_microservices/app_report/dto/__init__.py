# app_report/dto/__init__.py
from .adresse_dto import AddressDTO
from .building_component_dto import BuildingComponentDTO
from .complete_house_details_dto import CompleteHouseDetailsDTO
from .damage_details_dto import DamageDetailsDTO
from .owner_details_dto import OwnerDetailsDTO

from .hustype_dto import HustypeDTO
from .customer_report_dto import CustomerReportDTO
from .inspector_report_dto import InspectorReportDTO

__all__ = [
    "AddressDTO",
    "BuildingComponentDTO",
    "CompleteHouseDetailsDTO",
    "DamageDetailsDTO",
    "OwnerDetailsDTO",
    
    "HustypeDTO"
    "CustomerReportDTO"
    "InspectorReportDTO"
]
