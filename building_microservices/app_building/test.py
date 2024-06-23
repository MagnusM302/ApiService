import os
import sys
import unittest
import requests
import subprocess
import time
import logging

# Ensure correct path is set
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

class TestUserServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.start_services()
        cls.user_base_url = 'http://localhost:5000'
        cls.building_base_url = 'http://localhost:5005/api/buildings'
        cls.login_url = f'{cls.user_base_url}/api/users/login'
        cls.inspector_credentials = {
            "username": "tryk12",
            "password": "12345678"
        }
        cls.token = cls.get_auth_token(cls.inspector_credentials)

    @classmethod
    def start_services(cls):
        # Start UserService
        user_service_path = os.path.join(project_root, "user_microservices", "app_user", "runmain.py")
        cls.user_service_process = subprocess.Popen(
            ["python", user_service_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        cls.log_subprocess_output(cls.user_service_process.stdout)
        cls.log_subprocess_output(cls.user_service_process.stderr)
        
        # Start BuildingService
        building_service_path = os.path.join(project_root, "building_microservices", "app_building", "runmain.py")
        cls.building_service_process = subprocess.Popen(
            ["python", building_service_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        cls.log_subprocess_output(cls.building_service_process.stdout)
        cls.log_subprocess_output(cls.building_service_process.stderr)

        # Wait for the services to start
        cls.wait_for_service('http://localhost:5000/api/users/health', timeout=60)
        cls.wait_for_service('http://localhost:5005/api/buildings/health', timeout=60)

    @classmethod
    def wait_for_service(cls, url, timeout=60):
        """Wait for a service to be available"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return True
            except requests.ConnectionError:
                time.sleep(1)
        raise RuntimeError(f"Service at {url} did not start within {timeout} seconds")

    @classmethod
    def log_subprocess_output(cls, pipe):
        for line in iter(pipe.readline, b''):
            logging.info(line.decode().strip())

    @classmethod
    def tearDownClass(cls):
        cls.user_service_process.terminate()
        cls.building_service_process.terminate()
        cls.user_service_process.wait()
        cls.building_service_process.wait()

    @classmethod
    def get_auth_token(cls, credentials):
        response = requests.post(cls.login_url, json=credentials)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            logging.error(f"Failed to get auth token: {response.json()}")
            return None

    def test_get_building_details(self):
        address = "Strandvejen 100, 2900 Hellerup"  # Example address
        building_details = self.fetch_building_details(address)
        self.assertIsNotNone(building_details, "Failed to get building details")
        self.assertEqual(building_details['address'], address, "Address mismatch in building details")

    def fetch_building_details(self, address):
        url = f"{self.building_base_url}/fetch_building_details"
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'address': address}
        logging.info(f"Sending GET request to {url} with headers {headers} and params {params}")
        try:
            response = requests.get(url, headers=headers, params=params)
            logging.info(f"Response status: {response.status_code}, Response body: {response.text}")
            response.raise_for_status()
            building_details = response.json()
            if not building_details:
                raise ValueError("No building details found")
            return building_details
        except requests.RequestException as e:
            logging.error(f"Failed to fetch building details: {e}")
            return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
