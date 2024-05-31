from building_microservices.app_building.dal import BuildingRepository
from building_microservices.app_building.dtos.dto_converters import DTOConverters
from building_microservices.app_building.dtos import AddressDTO, AddressProcessor, HouseDetailsDTO, CompleteHouseDetailsDTO, BuildingDetailsDTO

class BuildingService:
    @staticmethod
    def get_address(address: str) -> AddressDTO:
        address_data = BuildingRepository.fetch_address(address)
        print(f"Address data received: {address_data}")  # Debug print
        
        if not address_data or 'data' not in address_data[0]:
            print("No address data found or invalid structure")
            raise ValueError("No address data found or invalid structure")
        
        address_dto = AddressProcessor.process_address_data(address_data[0]['data'])
        return address_dto
    
    @staticmethod
    def get_address_details(address_id: str):
        return BuildingRepository.fetch_address_details(address_id)

    @staticmethod
    def get_building_details(building_id: str) -> BuildingDetailsDTO:
        building_details = BuildingRepository.fetch_building_details(building_id)
        return DTOConverters.to_building_details_dto(building_details)

    @staticmethod
    def get_full_details(address: str) -> HouseDetailsDTO:
        house_details = BuildingRepository.get_full_details(address)
        return DTOConverters.to_house_details_dto(house_details)

    @staticmethod
    def get_complete_house_details(address: str) -> CompleteHouseDetailsDTO:
        complete_house_details = BuildingRepository.get_complete_house_details(address)
        return DTOConverters.to_complete_house_details_dto(complete_house_details)

    # CRUD operations using DTOs
    @staticmethod
    def create_house_details(house_details_dto: HouseDetailsDTO):
        house_details = DTOConverters.to_house_details(house_details_dto)
        BuildingRepository.create_house_details(house_details)

    @staticmethod
    def read_house_details(house_id: str) -> HouseDetailsDTO:
        house_details = BuildingRepository.read_house_details(house_id)
        if house_details:
            return DTOConverters.to_house_details_dto(house_details)
        return None

    @staticmethod
    def update_house_details(house_id: str, updated_details_dto: dict):
        updated_details = DTOConverters.to_house_details(HouseDetailsDTO(**updated_details_dto))
        BuildingRepository.update_house_details(house_id, updated_details.dict())

    @staticmethod
    def delete_house_details(house_id: str):
        BuildingRepository.delete_house_details(house_id)
