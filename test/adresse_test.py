import sys
import os
import unittest
import requests
from multiprocessing import Process
from time import sleep
from pymongo import MongoClient
import bcrypt
from enum import Enum
# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def run_user_service():
    from user_microservices.run import create_user_app
    app = create_user_app()
    app.run(port=5001, debug=True, use_reloader=False)

def run_building_service():
    from building_microservices.run import create_building_app
    app = create_building_app()
    app.run(port=5005, debug=True, use_reloader=False)

USER_SERVICE_URL = "http://localhost:5001"
BUILDING_SERVICE_URL = "http://localhost:5005"

USERNAME = "tryk12"
PASSWORD = "12345678"
ADDRESS = "kærvej 7, 9800"

class UserRole(Enum):
    INSPECTOR = 1
    CUSTOMER = 2

class TestBuildingService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the services
        cls.user_service_process = Process(target=run_user_service)
        cls.building_service_process = Process(target=run_building_service)
        
        cls.user_service_process.start()
        cls.building_service_process.start()
        
        sleep(30)  # Wait for the services to start

        # Connect to MongoDB using the same URI as in TestLoginFunctionality
        cls.client = MongoClient('mongodb+srv://buildingDBuser:$Skole1234@cluster0.dezwb5i.mongodb.net/BuildingReportsDB?retryWrites=true&w=majority')
        cls.db = cls.client['BuildingReportsDB']
        cls.users_collection = cls.db['users']

        # Create inspector user if not exists
        cls.inspector_credentials = {
            "username": USERNAME,
            "password": PASSWORD
        }
        cls.inspector_details = {
            "name": "Inspector User",
            "address": "123 Inspector St",
            "post_number": "1234",
            "phone": "12345678",
            "username": cls.inspector_credentials['username'],
            "email": "inspector@example.com",
            "role": UserRole.INSPECTOR.value,
            "password_hash": bcrypt.hashpw(cls.inspector_credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }
        if cls.users_collection.find_one({"username": cls.inspector_credentials['username']}) is None:
            cls.users_collection.insert_one(cls.inspector_details)

        # Log in to the user service to get a token
        login_url = f"{USER_SERVICE_URL}/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        for i in range(5):  # Retry mechanism to ensure login after services are fully up
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                break
            sleep(5)
        assert response.status_code == 200, f"Login failed: {response.json()}"
        cls.token = response.json()['token']
        print(f"Token: {cls.token}")

    @classmethod
    def tearDownClass(cls):
        # Clean up the database and stop the services
        cls.users_collection.delete_many({"username": cls.inspector_credentials['username']})
        
        cls.user_service_process.terminate()
        cls.user_service_process.join()
        
        cls.building_service_process.terminate()
        cls.building_service_process.join()

    # adresse_test.py
    def test_get_address(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        address_url = f"{BUILDING_SERVICE_URL}/api/get_address"
        params = {"address": ADDRESS}
        response = requests.get(address_url, headers=headers, params=params)
    
        print(f"Request URL: {response.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        self.assertEqual(response.status_code, 200, f"Failed to fetch address: {response.text}")
        address_data = response.json()
        self.assertNotEqual(len(address_data), 0, "Address data is empty")
        self.assertIn("id", address_data[0], "Address data is missing 'id'")
        self.assertIn("adgangsadresseid", address_data[0], "Address data is missing 'adgangsadresseid'")


if __name__ == "__main__":
    unittest.main()
