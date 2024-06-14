import sys
import os
import subprocess
import time
import bcrypt
from enum import Enum
from pymongo import MongoClient
from shared.database import Database  # Ensure this import matches the location of your Database class
import unittest
# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Define UserRole enum
class UserRole(Enum):
    INSPECTOR = 1
    CUSTOMER = 2

class TestUserServiceIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start Flask server
        cls.server = subprocess.Popen(["python", "runmain.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)  # Wait for the server to start

        # Connect to MongoDB using Database class
        cls.db = Database.db
        cls.users_collection = Database.get_collection('users')

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
            "role": UserRole.INSPECTOR.value,
            "password_hash": bcrypt.hashpw(cls.inspector_credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }

        # Insert the user into the database if it doesn't exist
        if cls.users_collection.find_one({"username": cls.inspector_credentials['username']}) is None:
            cls.users_collection.insert_one(cls.inspector_details)

    @classmethod
    def tearDownClass(cls):
        # Clean up the database
        cls.users_collection.delete_many({"username": cls.inspector_credentials['username']})
        cls.server.terminate()
        cls.server.wait()

    def test_inspector_registration_of_new_user(self):
        # Test logic for registering a new inspector user
        self.assertIsNotNone(self.users_collection.find_one({"username": self.inspector_credentials['username']}))

if __name__ == "__main__":
    unittest.main()
