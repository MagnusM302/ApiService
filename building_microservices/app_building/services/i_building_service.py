# building_microservices/app_building/services/interfaces.py

from ..dtos.address_dto import AddressDTO
from ..dtos.building_details_dto import BuildingDetailsDTO
from abc import ABC, abstractmethod

class IBuildingService(ABC):
    @abstractmethod
    def get_address(self, address: str) -> AddressDTO:
        pass

    @abstractmethod
    def get_address_details(self, address_id: str) -> AddressDTO:
        pass

    @abstractmethod
    def get_building_details(self, building_id: str) -> BuildingDetailsDTO:
        pass
    @abstractmethod
    def get_complete_house_details(self, address: str) -> BuildingDetailsDTO:
        pass
    @abstractmethod
    def get_building_square_meters(self, building_id: str) -> BuildingDetailsDTO:
        pass
    