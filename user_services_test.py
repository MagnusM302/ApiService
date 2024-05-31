import unittest
import requests
import subprocess
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from user_microservices.app_user.enums import UserRole

class TestUserServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Flask server
        cls.server = subprocess.Popen(["python", "runmain.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for the server to start

        # Connect to MongoDB
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['mydatabase']
        cls.users_collection = cls.db['users']

        # Create inspector user if not exists
        cls.inspector_credentials = {
            "username": "tryk12",
            "password": "12345678"
        }
        cls.inspector_details = {
            "name": "Inspector User",
            "address": "123 Inspector St",
            "post_number": "1234",
            "phone": "12345678",
            "username": cls.inspector_credentials['username'],
            "email": "inspector@example.com",
            "role": UserRole.Inspector.value,
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
        self.login_url = f'{self.base_url}/login'
        self.register_url = f'{self.base_url}/register'
        self.new_user_details = {
            "name": "New User",
            "address": "123 Main St",
            "post_number": "1234",
            "phone": "12345678",
            "username": "newuser",
            "password": "newuserpassword",
            "email": "newuser@example.com",
            "role": "Inspector"  # Ensure this matches the UserRole name exactly
        }

    def test_inspector_registration_of_new_user(self):
        # Log in as inspector
        login_response = requests.post(self.login_url, json=self.inspector_credentials)
        print(f"Login Response Status Code: {login_response.status_code}")
        print(f"Login Response Data: {login_response.text}")

        self.assertEqual(login_response.status_code, 200, "Inspector login failed")
        token = login_response.json().get('token')
        self.assertIsNotNone(token, "No token received from inspector login")

        # Use inspector token to register a new user
        headers = {'Authorization': f'Bearer {token}'}
        register_response = requests.post(self.register_url, json=self.new_user_details, headers=headers)

        # Print response status code and data for debugging
        print(f"Register Response Status Code: {register_response.status_code}")
        print(f"Register Response Data: {register_response.text}")

        self.assertEqual(register_response.status_code, 201, "Failed to register new user")
        if register_response.status_code == 201:
            response_data = register_response.json()
            self.assertIn('user_id', response_data, "User ID not returned in registration response")

if __name__ == '__main__':
    unittest.main()
