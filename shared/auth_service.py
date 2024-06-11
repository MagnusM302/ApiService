import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, current_app
from user_microservices.app_user.models import UserRole
from functools import wraps
from .config import ALLOWED_SERVICE_IDS


class JWTService:
    secret_key = "your_secret_key_here"  # Statisk hemmelig nøgle for demonstration
    algorithm = 'HS256'

    @staticmethod
    def generate_token(user_id, role, expires_in=24):
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in)
        }
        return jwt.encode(payload, JWTService.secret_key, algorithm=JWTService.algorithm)
    
    @staticmethod
    def generate_system_token(service_id):
        if service_id not in ALLOWED_SERVICE_IDS:
            raise ValueError("Unauthorized service request")
        payload = {
            "service_id": service_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(payload, JWTService.secret_key, algorithm='HS256')

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'message': 'A valid token is missing'}), 403

            token = None
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]  # Fjern 'Bearer ' præfikset
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
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    return jsonify({'message': 'A valid token is missing'}), 403

                token = None
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]  # Fjern 'Bearer ' præfikset
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
