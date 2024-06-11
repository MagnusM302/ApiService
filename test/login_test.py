import unittest
import requests
from multiprocessing import Process
from time import sleep
from pymongo import MongoClient
import bcrypt
from enum import Enum

def run_flask_app():
    from user_microservices.run import create_user_app  # Update this import according to your actual import paths
    app = create_user_app()
    app.run(port=5001, debug=True, use_reloader=False)

# Define UserRole enum
class UserRole(Enum):
    INSPECTOR = 1
    CUSTOMER = 2

class TestLoginFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app in a separate process
        cls.process = Process(target=run_flask_app)
        cls.process.start()
        sleep(5)  # Wait a moment for the server to start

        # Connect to MongoDB using Database class
        cls.client = MongoClient('mongodb+srv://buildingDBuser:$Skole1234@cluster0.dezwb5i.mongodb.net/BuildingReportsDB?retryWrites=true&w=majority')
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
            "post_number": "1234",
            "phone": "12345678",
            "username": cls.inspector_credentials['username'],
            "email": "inspector@example.com",
            "role": UserRole.INSPECTOR.value,
            "password_hash": bcrypt.hashpw(cls.inspector_credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }
        if cls.users_collection.find_one({"username": cls.inspector_credentials['username']}) is None:
            cls.users_collection.insert_one(cls.inspector_details)

    @classmethod
    def tearDownClass(cls):
        cls.users_collection.delete_many({"username": cls.inspector_credentials['username']})
        cls.process.terminate()
        cls.process.join()

    def test_login_with_valid_credentials(self):
        """ Test logging in with correct credentials """
        response = requests.post(
            'http://localhost:5001/login',
            json={'username': 'tryk12', 'password': '12345678'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)

    def test_login_with_invalid_credentials(self):
        """ Test logging in with incorrect credentials """
        response = requests.post(
            'http://localhost:5001/login',
            json={'username': 'tryk12', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())

if __name__ == '__main__':
    unittest.main()
