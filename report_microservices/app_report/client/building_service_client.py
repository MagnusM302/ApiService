import os
import sys
# Ensure correct path is set
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(project_root)

import logging
import requests
from building_microservices.app_building.dtos import AddressDTO, BuildingDetailsDTO

class BuildingServiceClient:
    def __init__(self, base_url: str = "http://localhost:5005/api/buildings", token: str = None):
        self.base_url = base_url
        self.token = token

    def get_address(self, address_query: str) -> AddressDTO:
        address_query = address_query.strip()
        url = f"{self.base_url}/address"
        headers = self.get_headers()
        params = {'address': address_query}
        logging.info(f"Sending GET request to {url} with headers {headers} and params {params}")
        try:
            response = requests.get(url, headers=headers, params=params)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            address_data = response.json()
            if not address_data:
                raise ValueError("No address data found")
            return AddressDTO(**address_data)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch address: {e}")
            raise

    def get_address_details(self, address_id: str) -> AddressDTO:
        url = f"{self.base_url}/address/{address_id}"
        headers = self.get_headers()
        logging.info(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            address_details = response.json()
            if not address_details:
                raise ValueError(f"No address details found for ID: {address_id}")
            return AddressDTO(**address_details)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch address details: {e}")
            raise

    def get_building_details(self, building_id: str) -> BuildingDetailsDTO:
        url = f"{self.base_url}/building/{building_id}"
        headers = self.get_headers()
        logging.info(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            building_data = response.json()
            if not building_data:
                raise ValueError("No building data found")
            return BuildingDetailsDTO(**building_data)
        except requests.RequestException as e:
            logging.error(f"Failed to get building details: {e}")
            raise

    def get_headers(self):
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        logging.info(f"Generated headers: {headers}")
        return headers

    def set_token(self, token: str):
        self.token = token
        logging.info(f"Token set: {self.token}")

    def fetch_building_details(self, address):
        address = address.strip()
        url = f"{self.base_url}/fetch_building_details"
        headers = self.get_headers()
        params = {'address': address}
        logging.info(f"Sending GET request to {url} with headers {headers} and params {params}")
        try:
            response = requests.get(url, headers=headers, params=params)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            building_details = response.json()
            if not building_details:
                raise ValueError("No building details found")
            return BuildingDetailsDTO(**building_details)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch building details: {e}")
            return None