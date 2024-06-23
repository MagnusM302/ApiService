# building_microservices/app_building/services/building_service.py
import logging
from ..dal.i_building_repository import IBuildingRepository
from ..dtos import AddressDTO, BuildingDetailsDTO
from ..models import Address, BuildingDetails

class BuildingService:
    def __init__(self, building_repository: IBuildingRepository):
        self.building_repository = building_repository

    def get_address(self, address: str) -> AddressDTO:
        logging.info(f"Service: Getting address for: {address}")
        try:
            address_model: Address = self.building_repository.fetch_address(address)
            return AddressDTO(**address_model.__dict__)
        except Exception as e:
            logging.error(f"Service: Error getting address: {e}")
            raise

    def get_address_details(self, address_id: str) -> AddressDTO:
        logging.info(f"Service: Getting address details for ID: {address_id}")
        try:
            address_model: Address = self.building_repository.fetch_address_details(address_id)
            return AddressDTO(**address_model.__dict__)
        except Exception as e:
            logging.error(f"Service: Error getting address details: {e}")
            raise

    def get_building_details(self, building_id: str) -> BuildingDetailsDTO:
        logging.info(f"Service: Getting building details for ID: {building_id}")
        try:
            building_model: BuildingDetails = self.building_repository.fetch_building_details(building_id)
            return BuildingDetailsDTO(**building_model.__dict__)
        except Exception as e:
            logging.error(f"Service: Error getting building details: {e}")
            raise

    def fetch_complete_building_details(self, address: str) -> BuildingDetailsDTO:
        logging.info(f"Service: Fetching complete building details for address: {address}")
        try:
            # Step 1: Get address information
            address_dto = self.get_address(address)
            logging.info(f"Fetched address DTO: {address_dto}")

            # Step 2: Get address details using the adgangsadresseid from address_dto
            address_details_dto = self.get_address_details(address_dto.adgangsadresseid)
            logging.info(f"Fetched address details DTO: {address_details_dto}")

            # Step 3: Get building details using the adgangsadresseid from address_details_dto
            building_details_dto = self.get_building_details(address_details_dto.adgangsadresseid)
            logging.info(f"Fetched building details DTO: {building_details_dto}")

            return building_details_dto
        except Exception as e:
            logging.error(f"Service: Error fetching complete building details: {e}")
            raise