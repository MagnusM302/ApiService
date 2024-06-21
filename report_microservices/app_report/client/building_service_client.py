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
        print(f"Sending GET request to {url} with headers {headers} and params {params}")
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            return response.json()  # Return the response as JSON
        except requests.RequestException as e:
            print(f"Failed to autocomplete address: {e}")
            return None

    def get_complete_building_details(self, address):
        url = f"{self.base_url}/buildings/address"
        headers = self.get_headers()
        print(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            print(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            return response.json()  # Return the response as JSON
        except requests.RequestException as e:
            print(f"Failed to get complete building details: {e}")
            return None

    def get_building_details(self, building_id: str):
        url = f"{self.base_url}/buildings/building/{building_id}"
        headers = self.get_headers()
        print(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            print(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            building_data = response.json()
            if not building_data:
                print("No building data found")
                raise ValueError("No building data found")
            return building_data  # Return the response as JSON
        except requests.RequestException as e:
            print(f"Failed to get building details: {e}")
            return None

    def get_building_square_meters(self, building_id: str):
        url = f"{self.base_url}/buildings/building/{building_id}/square_meters"
        headers = self.get_headers()
        print(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            print(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            return response.json()  # Return the response as JSON
        except requests.RequestException as e:
            print(f"Failed to get building square meters: {e}")
            return None

    def get_headers(self):
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        print(f"Generated headers: {headers}")
        return headers

    def set_token(self, token: str):
        self.token = token
