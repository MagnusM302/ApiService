import requests
from building_microservices.app_building.dtos import AddressDTO, BuildingDetailsDTO
from shared.enums import (
    Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale,
    BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
)
import logging

class BuildingServiceClient:
    def __init__(self, base_url: str = "http://localhost:5005/api", token: str = None):
        self.base_url = base_url
        self.token = token

    def get_headers(self):
        return {'Authorization': f'Bearer {self.token}'} if self.token else {}

    def get_building_details(self, building_id: str) -> BuildingDetailsDTO:
        logging.debug(f"Fetching building details for ID: {building_id} from {self.base_url}/building/{building_id}")
        try:
            response = requests.get(f"{self.base_url}/building/{building_id}", headers=self.get_headers())
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()
            building_data = response.json()

            # Convert string enums to actual Enum types
            building_data['byg021BygningensAnvendelse'] = BygningensAnvendelse(building_data['byg021BygningensAnvendelse'])
            building_data['byg056Varmeinstallation'] = Varmeinstallation(building_data['byg056Varmeinstallation'])
            building_data['byg032YdervæggensMateriale'] = YdervæggensMateriale(building_data['byg032YdervæggensMateriale'])
            building_data['byg033Tagdækningsmateriale'] = TagdækningsMateriale(building_data['byg033Tagdækningsmateriale'])
            building_data['byg037KildeTilBygningensMaterialer'] = KildeTilBygningensMaterialer(building_data['byg037KildeTilBygningensMaterialer'])
            building_data['byg058SupplerendeVarme'] = SupplerendeVarme(building_data['byg058SupplerendeVarme'])

            logging.debug(f"Building details fetched and converted: {building_data}")

            return BuildingDetailsDTO(**building_data)
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 404:
                logging.error(f"Building with ID {building_id} not found")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

    def get_address_details(self, address_id: str) -> AddressDTO:
        logging.debug(f"Fetching address details for ID: {address_id} from {self.base_url}/address/{address_id}")
        try:
            response = requests.get(f"{self.base_url}/address/{address_id}", headers=self.get_headers())
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()
            address_data = response.json()
            logging.debug(f"Address details fetched: {address_data}")
            return AddressDTO(**address_data)
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 404:
                logging.error(f"Address with ID {address_id} not found")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise
