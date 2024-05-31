import time
import unittest
import threading
from waitress import serve
from flask import Flask
from flask_cors import CORS
from user_microservices.app_user.controllers import setup_routes as setup_user_routes
from building_microservices.app_building.controllers import setup_routes as setup_building_routes
from invoice_microservices.app_invoice.controllers import setup_routes as setup_invoice_routes
import requests
from building_microservices.app_building.services import BuildingService

def start_app(app, port):
    serve(app, host='0.0.0.0', port=port)

def setup_logging(service_name):
    import logging
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(f'{service_name}.log', maxBytes=10240, backupCount=5)
    file_formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

def setup_user_service():
    app = Flask("UserService")
    CORS(app)
    logger = setup_logging("UserService")
    setup_user_routes(app, None)
    logger.debug("UserService Setup Complete")
    return app

def setup_building_service():
    app = Flask("BuildingService")
    CORS(app)
    logger = setup_logging("BuildingService")
    building_service = BuildingService()
    setup_building_routes(app, building_service)
    logger.debug("BuildingService Setup Complete")
    return app

def setup_invoice_service():
    app = Flask("InvoiceService")
    CORS(app)
    logger = setup_logging("InvoiceService")
    setup_invoice_routes(app, None)
    logger.debug("InvoiceService Setup Complete")
    return app

services = {
    'user': (setup_user_service(), 5000),
    'building': (setup_building_service(), 5001),
    'invoice': (setup_invoice_service(), 5002)
}

threads = []
for service_name, (app, port) in services.items():
    thread = threading.Thread(target=start_app, args=(app, port))
    thread.start()
    threads.append(thread)
    print(f"{service_name} service started on port {port}")

time.sleep(5)

class TestBuildingService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = 'http://localhost:5000/login'
        cls.credentials = {
            "username": "tryk12",
            "password": "12345678"
        }
        
        cls.base_url = "http://localhost:5001/api/get_address"
        cls.address = "Kærvej 7, 9800"
        
        print("Attempting login...")
        login_response = requests.post(cls.login_url, json=cls.credentials)
        print(f"Login response status: {login_response.status_code}")
        print(f"Login response data: {login_response.json()}")
        
        assert login_response.status_code == 200, "Login failed"
        cls.token = login_response.json().get('token')
        assert cls.token is not None, "No token received from login"
        cls.headers = {
            'Authorization': f'Bearer {cls.token}',
            'Content-Type': 'application/json'
        }
        print(f"Received token: {cls.token}")

    def test_get_address_success(self):
        """Test successful retrieval of address details with valid JWT."""
        print("Testing get_address_success...")
        response = requests.get(self.base_url, params={"address": self.address}, headers=self.headers)
        print(f'Response Status Code: {response.status_code}')
        print(f'Response Data: {response.text}')
        self.assertEqual(response.status_code, 200, "Failed to get address details")

    def test_get_address_unauthorized(self):
        """Test retrieval of address details with intentionally invalid JWT."""
        print("Testing get_address_unauthorized...")
        bad_headers = {
            'Authorization': 'Bearer invalid_jwt_token.this_is_not_valid_base64.anything',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.base_url, params={"address": self.address}, headers=bad_headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.text}")
        self.assertEqual(response.status_code, 401, "Unauthorized request did not fail as expected")

    def test_get_address_details_with_valid_token(self):
        """Test retrieval of address details using id with valid JWT."""
        print("Testing get_address_details_with_valid_token...")
        address_response = requests.get(self.base_url, params={"address": self.address}, headers=self.headers)
        print(f"Address Response Status Code: {address_response.status_code}")
        print(f"Address Response Data: {address_response.text}")
        
        self.assertEqual(address_response.status_code, 200, "Failed to get address details")
        
        address_data = address_response.json()
        print(f"Parsed Address Data: {address_data}")

        # Use 'id' field for the next request
        address_id = address_data.get('id')
        print(f"Extracted address id: {address_id}")
        
        self.assertIsNotNone(address_id, "address id is None")
        
        details_url = f"http://localhost:5001/api/get_address_details"
        details_response = requests.get(details_url, params={"address_id": address_id}, headers=self.headers)
        print(f'Details Response Status Code: {details_response.status_code}')
        print(f'Details Response Data: {details_response.text}')
        
        self.assertEqual(details_response.status_code, 200, "Failed to get address details with address id")

if __name__ == '__main__':
    unittest.main()
