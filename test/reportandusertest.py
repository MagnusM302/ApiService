import sys
import os
import unittest
import requests
from multiprocessing import Process
from time import sleep
from unittest.mock import patch, MagicMock
from enum import Enum


def add_project_to_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

add_project_to_sys_path()
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from building_microservices.app_building.dtos import AddressDTO, BuildingDetailsDTO
# Import necessary modules
from user_microservices.app_user.services.user_service import UserService
from user_microservices.app_user.dal.user_repository import UserRepository
from user_microservices.app_user.controller.user_controller import create_user_blueprint
from building_microservices.app_building.services.building_service import BuildingService
from building_microservices.app_building.dal.building_repository import BuildingRepository
from building_microservices.app_building.controllers.building_controller import create_building_blueprint
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.services.report_services import ReportService
from shared.database import db_instance

def run_user_service():
    from flask import Flask
    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    user_repository = UserRepository(db_instance)
    user_service = UserService(user_repository)
    user_blueprint = create_user_blueprint(user_service)
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def run_building_service():
    from flask import Flask
    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    building_repository = BuildingRepository()
    building_service = BuildingService(building_repository)
    building_blueprint = create_building_blueprint(building_service)
    app.register_blueprint(building_blueprint, url_prefix='/api/buildings')
    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)

def run_report_service():
    from flask import Flask
    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
    report_repository = ReportRepository(db_instance)
    report_service = ReportService(building_service_client, report_repository)
    report_blueprint = create_report_blueprint(report_service)
    app.register_blueprint(report_blueprint, url_prefix='/api/reports')
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

USER_SERVICE_URL = "http://localhost:5000"
BUILDING_SERVICE_URL = "http://localhost:5005"
REPORT_SERVICE_URL = "http://localhost:5006"

USERNAME = "tryk12"
PASSWORD = "12345678"
ADDRESS = "kærvej 7, 9800"

class UserRole(Enum):
    INSPECTOR = 1
    CUSTOMER = 2

class TestBuildingService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_service_process = Process(target=run_user_service)
        cls.building_service_process = Process(target=run_building_service)
        cls.report_service_process = Process(target=run_report_service)
        
        cls.user_service_process.start()
        cls.building_service_process.start()
        cls.report_service_process.start()
        
        sleep(40)  # Give the services more time to start

        cls.inspector_credentials = {
            "username": USERNAME,
            "password": PASSWORD
        }

        login_url = f"{USER_SERVICE_URL}/api/users/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        for i in range(5):
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                break
            sleep(5)
        assert response.status_code == 200, f"Login failed: {response.json()}"
        cls.token = response.json()['token']
        print(f"Token: {cls.token}")

        add_project_to_sys_path()
        from report_microservices.app_report.client.building_service_client import BuildingServiceClient
        cls.building_service_client = BuildingServiceClient(token=cls.token)

    @classmethod
    def tearDownClass(cls):
        cls.user_service_process.terminate()
        cls.user_service_process.join()
        
        cls.building_service_process.terminate()
        cls.building_service_process.join()

        cls.report_service_process.terminate()
        cls.report_service_process.join()

    def test_get_address(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{BUILDING_SERVICE_URL}/api/buildings/address", headers=headers, params={'address': ADDRESS})
        self.assertEqual(response.status_code, 200, f"Failed to fetch address: {response.json()}")
        
        address_data = response.json()
        self.assertIsInstance(address_data, dict, "Expected response to be a dict")
        self.assertIn('vejnavn', address_data, "Expected 'vejnavn' key in the address item")
        self.assertIn('husnr', address_data, "Expected 'husnr' key in the address item")

    def test_get_address_details(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{BUILDING_SERVICE_URL}/api/buildings/address/0a3f50c8-2902-32b8-e044-0003ba298018", headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to fetch address details: {response.json()}")
        
        details_data = response.json()
        self.assertIn('id', details_data, "Expected 'id' key in the address details")
        self.assertIn('vejnavn', details_data, "Expected 'vejnavn' key in the address details")
        self.assertIn('husnr', details_data, "Expected 'husnr' key in the address details")

    def test_get_building_details(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{BUILDING_SERVICE_URL}/api/buildings/building/3d90f674-e642-4516-b4a1-45f2617b561f", headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to fetch building details: {response.json()}")
        
        details_data = response.json()
        self.assertIn('id', details_data, "Expected 'id_lokalId' key in the building details")
        self.assertIn('byg007Bygningsnummer', details_data, "Expected 'byg007Bygningsnummer' key in the building details")
        self.assertIn('byg021BygningensAnvendelse', details_data, "Expected 'byg021BygningensAnvendelse' key in the building details")
    
    
if __name__ == '__main__':
    unittest.main()
