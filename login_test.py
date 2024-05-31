import unittest
import requests
from multiprocessing import Process
from time import sleep

def run_flask_app():
    from user_microservices.run import create_user_app  # Update this import according to your actual import paths
    app = create_user_app()
    app.run(port=5001, debug=True, use_reloader=False)

class TestLoginFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app in a separate process
        cls.process = Process(target=run_flask_app)
        cls.process.start()
        sleep(1)  # Wait a moment for the server to start

    @classmethod
    def tearDownClass(cls):
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