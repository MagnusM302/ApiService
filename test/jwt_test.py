import unittest
import jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify
from user_microservices.app_user.models import UserRole
from shared.auth_service import JWTService

class TestJWTService(unittest.TestCase):

    def setUp(self):
        self.user_id = "12345"
        self.role = UserRole.INSPECTOR.value
        self.secret_key = "your_secret_key_here"
        self.app = Flask(__name__)

        # Create a test route to test token validation
        @self.app.route('/protected')
        @JWTService.token_required
        def protected():
            return jsonify({'message': 'Token is valid'})

        self.client = self.app.test_client()

    def test_generate_token(self):
        token = JWTService.generate_token(self.user_id, self.role)
        decoded_token = jwt.decode(token, self.secret_key, algorithms=[JWTService.algorithm])
        
        self.assertEqual(decoded_token["sub"], self.user_id)
        self.assertEqual(decoded_token["role"], self.role)

    def test_expired_token(self):
        expired_token = jwt.encode(
            {
                "sub": self.user_id,
                "role": self.role,
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) - timedelta(hours=1)
            },
            self.secret_key,
            algorithm=JWTService.algorithm
        )

        headers = {"Authorization": expired_token}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token expired', response.json['message'])

    def test_invalid_token(self):
        invalid_token = "invalid.token.value"
        headers = {"Authorization": invalid_token}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid token', response.json['message'])

    def test_valid_token(self):
        token = JWTService.generate_token(self.user_id, self.role)
        headers = {"Authorization": token}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is valid', response.json['message'])

if __name__ == '__main__':
    unittest.main()
