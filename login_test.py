import unittest
import requests
import threading
from time import sleep
from flask import request
from user_microservices.run import create_user_app  # Make sure this import is correct

def run_flask_app(app):
    app.run(port=5000, use_reloader=False)

class TestLoginFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Flask server in a background thread
        cls.app = create_user_app()
        cls.app.debug = True
        cls.app.add_url_rule('/shutdown', 'shutdown', cls.shutdown)  # Adding shutdown route
        cls.server = threading.Thread(target=run_flask_app, args=(cls.app,))
        cls.server.start()
        print("Server started")

    @classmethod
    def tearDownClass(cls):
        # Ensure the server is stopped after tests
        requests.get('http://localhost:5000/shutdown')
        cls.server.join()
        print("Server stopped")

    @staticmethod
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def setUp(self):
        self.base_url = 'http://localhost:5000'
        self.login_url = f'{self.base_url}/login'
        self.valid_credentials = {
            "username": "tryk12",
            "password": "12345678"
        }
        self.invalid_credentials = {
            "username": "wrongUser",
            "password": "wrongPassword"
        }

    def test_valid_login(self):
        # Testing valid login
        response = requests.post(self.login_url, json=self.valid_credentials)
        self.assertEqual(response.status_code, 200, "Failed to login with valid credentials")
        self.assertIsNotNone(response.json().get('token'), "Token not received on valid login")

    def test_invalid_login(self):
        # Testing invalid login
        response = requests.post(self.login_url, json=self.invalid_credentials)
        self.assertEqual(response.status_code, 401, "Incorrect status code for invalid credentials")
        self.assertIn("error", response.json(), "Error message not received on invalid login")

if __name__ == '__main__':
    unittest.main()
