import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, current_app
from user_microservices.app_user.models import UserRole
from functools import wraps
from config import ALLOWED_SERVICE_IDS

class JWTService:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, user_id, role, expires_in=24):
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_system_token(self, service_id):
        if service_id not in ALLOWED_SERVICE_IDS:
            raise ValueError("Unauthorized service request")
        payload = {
            "service_id": service_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def system_token_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            system_token = request.headers.get('System-Authorization')
            if not system_token:
                return jsonify({'message': 'Missing system authorization token'}), 401

            try:
                decoded_token = jwt.decode(system_token, self.secret_key, algorithms=[self.algorithm])
                # Yderligere validering kan tilføjes her
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'System token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid system token'}), 401

            return f(*args, **kwargs)
        return decorated_function
    
    def decode_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def refresh_token(self, token):
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
        payload['exp'] = datetime.now(timezone.utc) + timedelta(hours=24)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'A valid token is missing'}), 403

            try:
                current_user = self.decode_token(token)
            except ValueError as e:
                return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 403

            return f(current_user, *args, **kwargs)
        return decorated

    def role_required(self, allowed_roles):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                token = request.headers.get('Authorization')
                if not token:
                    return jsonify({'message': 'A valid token is missing'}), 403

                try:
                    current_user = self.decode_token(token)
                    user_role = UserRole(current_user['role'])  # Antager at 'role' er gemt som en Enum værdi
                except Exception as e:
                    return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 403

                if user_role not in allowed_roles:
                    return jsonify({'message': 'Permission denied'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator
