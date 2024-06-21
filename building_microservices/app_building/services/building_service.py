# building_microservices/app_building/services/building_service.py

import logging
from ..models.address import Address
from ..models.building_details import BuildingDetails
from ..dal.i_building_repository import IBuildingRepository
from .i_building_service import IBuildingService
from ..dtos.address_dto import AddressDTO
from ..dtos.building_details_dto import BuildingDetailsDTO

from ..dtos.dto_converters import address_to_dto, building_details_to_dto
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme

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
    
    def get_complete_house_details(self, address: str) -> BuildingDetailsDTO:
        logging.info(f"Fetching complete house details for address: {address}")

        # Step 1: Fetch address autocomplete
        address_entity = self.repository.fetch_address(address)
        if not address_entity:
            logging.error("Failed to autocomplete address")
            raise ValueError("Failed to autocomplete address: No results")

        # Step 2: Fetch full address details
        address_id = address_entity.id
        address_full_details = self.repository.fetch_address_details(address_id)
        if not address_full_details:
            logging.error("Failed to get address details")
            raise ValueError("Failed to get address details")

        # Step 3: Fetch building details
        building_id = address_full_details.adgangsadresseid
        building_details = self.repository.fetch_building_details(building_id)
        if not building_details:
            logging.error("Failed to get building details")
            raise ValueError("Failed to get building details")

        # Step 4: Create DTO without static owner details and hustype
        complete_house_details_dto = BuildingDetailsDTO(
            id="generated_id",
            address=address,
            year_built=building_details.byg026Opførelsesår,
            total_area=building_details.byg038SamletBygningsareal,
            number_of_buildings=building_details.byg054AntalEtager,
            varmeinstallation=Varmeinstallation(building_details.byg056Varmeinstallation).value,
            ydervaegsmateriale=YdervæggensMateriale(building_details.byg032YdervæggensMateriale).value,
            tagdaekningsmateriale=TagdækningsMateriale(building_details.byg033Tagdækningsmateriale).value,
            bygningens_anvendelse=BygningensAnvendelse(building_details.byg021BygningensAnvendelse).value,
            kilde_til_bygningens_materialer=KildeTilBygningensMaterialer(building_details.byg037KildeTilBygningensMaterialer).value,
            supplerende_varme=SupplerendeVarme(building_details.byg058SupplerendeVarme).value,
           
        )

        logging.info(f"Complete house details DTO: {complete_house_details_dto}")
        return complete_house_details_dto

    
    def get_building_square_meters(self, building_id: str) -> BuildingDetailsDTO:
        # Simulate fetching building square meters details
        square_meters_data = {
            "id_lokalId": building_id,
            "samlet_bygningsareal": 200.0,
            "samlede_boligareal": 180.0,
            "bebygget_areal": 150.0
        }
        return BuildingDetailsDTO(**square_meters_data)