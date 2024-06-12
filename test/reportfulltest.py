import sys
import os
import unittest
import requests
from multiprocessing import Process
from time import sleep
from enum import Enum

def add_project_to_sys_path():
    import os
    import sys
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app_report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app_report'))
    if root_path not in sys.path:
        sys.path.append(root_path)
    if app_report_path not in sys.path:
        sys.path.append(app_report_path)

def run_user_service():
    add_project_to_sys_path()
    from user_microservices.run import create_user_app
    app = create_user_app()
    app.run(port=5001, debug=True, use_reloader=False)

def run_building_service():
    add_project_to_sys_path()
    from building_microservices.run import create_building_app
    app = create_building_app()
    app.run(port=5005, debug=True, use_reloader=False)

def run_report_service():
    add_project_to_sys_path()
    from report_microservices.run import create_app
    app = create_app()
    app.run(port=5006, debug=True, use_reloader=False)

USER_SERVICE_URL = "http://localhost:5001"
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

        login_url = f"{USER_SERVICE_URL}/login"
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
        self.assertIn('id_lokalId', details_data, "Expected 'id_lokalId' key in the building details")
        self.assertIn('byg007Bygningsnummer', details_data, "Expected 'byg007Bygningsnummer' key in the building details")
        self.assertIn('byg021BygningensAnvendelse', details_data, "Expected 'byg021BygningensAnvendelse' key in the building details")
    
    def test_get_building_square_meters(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{BUILDING_SERVICE_URL}/api/buildings/building/3d90f674-e642-4516-b4a1-45f2617b561f/square_meters", headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to fetch building square meters: {response.json()}")
        
        square_meters_data = response.json()
        self.assertIn('id_lokalId', square_meters_data, "Expected 'id_lokalId' key in the building square meters")
        self.assertIn('samlet_bygningsareal', square_meters_data, "Expected 'samlet_bygningsareal' key in the building square meters")
        self.assertIn('samlede_boligareal', square_meters_data, "Expected 'samlede_boligareal' key in the building square meters")
        self.assertIn('bebygget_areal', square_meters_data, "Expected 'bebygget_areal' key in the building square meters")

if __name__ == '__main__':
    unittest.main()
