import requests
import logging

class InvoiceServiceClient:
    def __init__(self, base_url: str = "http://localhost:5005/api", token: str = None):
        self.base_url = base_url
        self.token = token

    def get_building_square_meters(self, building_id: str):
        url = f"{self.base_url}/buildings/building/{building_id}/square_meters"
        headers = self.get_headers()
        logging.info(f"Sending GET request to {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to get building square meters: {e}")
            return None

    def get_headers(self):
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        logging.info(f"Generated headers: {headers}")
        return headers

    def set_token(self, token: str):
        self.token = token
