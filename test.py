import unittest
from flask import Flask, jsonify
from flask_testing import TestCase
from flask_cors import CORS
from shared.auth_service import JWTService

class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        CORS(app)
        app.config['TESTING'] = True

        @app.route('/protected')
        @JWTService.token_required
        def protected():
            return "Protected endpoint"

        @app.route('/open')
        def open_endpoint():
            return "Open endpoint"

        return app

    def test_open_endpoint(self):
        response = self.client.get('/open')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Open endpoint")

    def test_protected_endpoint_without_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 403)  # Opdateret til at forvente 403

    def test_protected_endpoint_with_token(self):
        # Opdateret til at inkludere 'role' argumentet
        valid_token = JWTService.generate_token({'user_id': '123'}, 'user')
        headers = {
            'Authorization': f'Bearer {valid_token}'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Protected endpoint")

if __name__ == '__main__':
    unittest.main()
