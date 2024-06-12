import requests
import logging
from building_microservices.app_building.dtos import AddressDTO, BuildingDetailsDTO

class BuildingServiceClient:
    def __init__(self, base_url: str = "http://localhost:5005/api", token: str = None):
        self.base_url = base_url
        self.token = token



    def get_address_autocomplete(self, address_query: str):
        url = f"{self.base_url}/buildings/address"
        headers = self.get_headers()
        params = {'address': address_query}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to autocomplete address: {e}")
            return None

    def get_address_details(self, address_id: str):
        url = f"{self.base_url}/buildings/address/{address_id}"
        headers = self.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to get address details: {e}")
            return None

    def get_building_details(self, building_id: str):
        url = f"{self.base_url}/buildings/building/{building_id}"
        headers = self.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to get building details: {e}")
            return None

    def get_building_square_meters(self, building_id: str):
        url = f"{self.base_url}/buildings/building/{building_id}/square_meters"
        headers = self.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to get building square meters: {e}")
            return None

    def get_headers(self):
        return {'Authorization': f'Bearer {self.token}'} if self.token else {}

    def set_token(self, token: str):
        self.token = token
