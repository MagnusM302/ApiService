# building_microservices/app_building/services/building_service.py

from ..models.address import Address
from ..models.building_details import BuildingDetails
from ..datalag.interface import IBuildingRepository
from .interfaces import IBuildingService
from ..dtos.address_dto import AddressDTO
from ..dtos.building_details_dto import BuildingDetailsDTO
from ..dtos.dto_converters import address_to_dto, building_details_to_dto
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale,BygningensAnvendelse,KildeTilBygningensMaterialer,SupplerendeVarme

class BuildingService(IBuildingService):
    def __init__(self, repository: IBuildingRepository):
        self.repository = repository

    def get_address(self, address: str) -> AddressDTO:
        address = self.repository.fetch_address(address)
        return address_to_dto(address)

    def get_address_details(self, address_id: str) -> AddressDTO:
        address = self.repository.fetch_address_details(address_id)
        return address_to_dto(address)

    def get_building_details(self, building_id: str) -> BuildingDetailsDTO:
        building_details = self.repository.fetch_building_details(building_id)
        return building_details_to_dto(building_details)
    
    def get_building_square_meters(self, building_id: str) -> BuildingDetailsDTO:
        # Simulate fetching building square meters details
        square_meters_data = {
            "id_lokalId": building_id,
            "samlet_bygningsareal": 200.0,
            "samlede_boligareal": 180.0,
            "bebygget_areal": 150.0
        }
        return BuildingDetailsDTO(**square_meters_data)