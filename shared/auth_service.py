import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, current_app
from user_microservices.app_user.models.user_role import UserRole
from functools import wraps
from .config import ALLOWED_SERVICE_IDS
from shared.custom_dotenv import load_env_variables

load_env_variables()

class JWTService:
    # Load the secret key from environment variables or use a default key
    secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    algorithm = 'HS256'

    @staticmethod
    def generate_token(user_id, role, expires_in=24):
        """
        Generate a JWT token for a user with a specific role.
        """
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in)
        }
        return jwt.encode(payload, JWTService.secret_key, algorithm=JWTService.algorithm)
    
    @staticmethod
    def generate_system_token(service_id):
        """
        Generate a system token for a specific service.
        """
        if service_id not in ALLOWED_SERVICE_IDS:
            raise ValueError("Unauthorized service request")
        payload = {
            "service_id": service_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(payload, JWTService.secret_key, algorithm=JWTService.algorithm)

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            """
            Decorator to ensure the request has a valid JWT token.
            """
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'message': 'A valid token is missing'}), 403

            token = None
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]  # Remove 'Bearer ' prefix
            else:
                return jsonify({'message': 'Invalid token format'}), 403

            try:
                decoded_token = jwt.decode(token, JWTService.secret_key, algorithms=[JWTService.algorithm])
                print(f"Decoded Token: {decoded_token}")  # Log decoded token
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
            except Exception as e:
                print(f"Token decode error: {str(e)}")
                return jsonify({'message': 'Invalid token'}), 401

            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def role_required(allowed_roles):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                """
                Decorator to ensure the request has a valid JWT token and the correct user role.
                """
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    return jsonify({'message': 'A valid token is missing'}), 403

                token = None
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]  # Remove 'Bearer ' prefix
                else:
                    return jsonify({'message': 'Invalid token format'}), 403

                try:
                    decoded_token = jwt.decode(token, JWTService.secret_key, algorithms=[JWTService.algorithm])
                    user_role = decoded_token['role']
                    print(f"Decoded Token: {decoded_token}")  # Log decoded token
                except jwt.ExpiredSignatureError:
                    return jsonify({'message': 'Token expired'}), 401
                except jwt.InvalidTokenError:
                    return jsonify({'message': 'Invalid token'}), 401
                except Exception as e:
                    print(f"Token decode error: {str(e)}")
                    return jsonify({'message': 'Invalid token'}), 401

                if user_role not in allowed_roles:
                    return jsonify({'message': 'Permission denied'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator
# shared/auth_service.py
import requests
from requests.exceptions import RequestException

# shared/auth_service.py
import requests
from requests.exceptions import RequestException

def request_system_token(service_id):
    """
    Hent et systemtoken fra User Service.
    """
    print("Sending POST request to generate system token...")
    try:
        response = requests.post(
            'http://localhost:5000/api/users/system-token', 
            json={'service_id': service_id}
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        if response.status_code == 200:
            return response.json()['system_token']
        else:
            raise ValueError("Failed to get system token")
    except RequestException as e:
        print(f"Request failed: {e}")
        raise
