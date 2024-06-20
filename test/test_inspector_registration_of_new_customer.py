import os
import sys

# Import the function to start the user service
def add_project_to_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

add_project_to_sys_path()
import time
import requests
import unittest
import subprocess
from pymongo import MongoClient
import bcrypt
from user_microservices.app_user.models.user_role import UserRole

# Import the function to start the user service


from runmain import run_user_http, wait_for_service

class TestUserServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Flask server
        cls.server = subprocess.Popen(["python", "runmain.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for the server to start

        # Connect to MongoDB with SSL enabled
        cls.client = MongoClient(
            'mongodb+srv://buildingDBuser:$Skole1234@cluster0.dezwb5i.mongodb.net/BuildingReportsDB?retryWrites=true&w=majority',
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        cls.db = cls.client['BuildingReportsDB']
        cls.users_collection = cls.db['users']

        # Create inspector user if not exists
        cls.inspector_credentials = {
            "username": "tryk12",
            "password": "12345678"
        }
        cls.inspector_details = {
            "name": "Inspector User",
            "address": "123 Inspector St",
            "post_number": "8234",
            "phone": "12345678",
            "username": cls.inspector_credentials['username'],
            "email": "inspector@example.com",
            "role": UserRole.INSPECTOR.value,
            "password_hash": bcrypt.hashpw(cls.inspector_credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }

        # Check if inspector user already exists
        inspector_user = cls.users_collection.find_one({"username": cls.inspector_credentials['username']})
        if not inspector_user:
            cls.users_collection.insert_one(cls.inspector_details)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()  # Stop the Flask server
        cls.server.wait()  # Ensure the server process has terminated
        cls.client.close()

    def setUp(self):
        self.base_url = 'http://localhost:5000'
        self.login_url = f'{self.base_url}/api/users/login'
        self.register_url = f'{self.base_url}/api/users/register'
        self.new_user_details = {
            "name": "New Customer",
            "address": "123 Main St",
            "post_number": "1234",
            "phone": "12345678",
            "username": "newcustomer",
            "password": "newcustomerpassword",
            "email": "newcustomer@example.com",
            "role": UserRole.CUSTOMER.name  # Ensure this matches the UserRole name exactly
        }

    def test_inspector_registration_of_new_customer(self):
        # Log in as inspector
        login_response = requests.post(self.login_url, json=self.inspector_credentials)
        print(f"Login Response Status Code: {login_response.status_code}")
        print(f"Login Response Data: {login_response.text}")

        self.assertEqual(login_response.status_code, 200, "Inspector login failed")
        token = login_response.json().get('token')
        self.assertIsNotNone(token, "No token received from inspector login")

        # Use inspector token to register a new customer
        headers = {'Authorization': f'Bearer {token}'}
        register_response = requests.post(self.register_url, json=self.new_user_details, headers=headers)

        # Print response status code and data for debugging
        print(f"Register Response Status Code: {register_response.status_code}")
        print(f"Register Response Data: {register_response.text}")

        self.assertEqual(register_response.status_code, 201, "Failed to register new customer")
        if register_response.status_code == 201:
            response_data = register_response.json()
            self.assertIn('user_id', response_data, "User ID not returned in registration response")

if __name__ == '__main__':
    unittest.main()
