from abc import ABC, abstractmethod
from ..models import Address, BuildingDetails

class IBuildingRepository(ABC):

    @abstractmethod
    def fetch_address(self, address: str) -> Address:
        pass

    @abstractmethod
    def fetch_address_details(self, address_id: str) -> Address:
        pass

    @abstractmethod
    def fetch_building_details(self, building_id: str) -> BuildingDetails:
        pass
