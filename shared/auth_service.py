import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify
from functools import wraps
import logging
from .config import JWT_SECRET_KEY, ALLOWED_SERVICE_IDS

class JWTService:
    secret_key = JWT_SECRET_KEY
    algorithm = 'HS256'

    @staticmethod
    def generate_token(user_id, role, expires_in=24):
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in)
        }
        token = jwt.encode(payload, JWTService.secret_key, algorithm=JWTService.algorithm)
        logging.info(f"Generated token for user_id {user_id} with role {role}")
        return token
    
    @staticmethod
    def generate_system_token(service_id):
        if service_id not in ALLOWED_SERVICE_IDS:
            raise ValueError("Unauthorized service request")
        payload = {
            "service_id": service_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        token = jwt.encode(payload, JWTService.secret_key, algorithm=JWTService.algorithm)
        logging.info(f"Generated system token for service_id {service_id}")
        return token

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                logging.error("Authorization header is missing.")
                return jsonify(message="Authorization header is missing."), 403
        
            try:
            # Assuming the token includes the 'Bearer' prefix
                token = token.split(" ")[1]
                decoded_token = jwt.decode(token, JWTService.secret_key, algorithms=[JWTService.algorithm])
                logging.info(f"Decoded token: {decoded_token}")
            except IndexError:
                logging.error("Token format is incorrect. Expected 'Bearer {token}'.")
                return jsonify(message="Token format is incorrect."), 400
            except jwt.ExpiredSignatureError:
                logging.error("Token has expired.")
                return jsonify(message="Token has expired."), 401
            except jwt.InvalidTokenError as e:
                logging.error(f"Invalid token: {e}")
                return jsonify(message="Invalid token."), 401
            except Exception as e:
                logging.error(f"Unexpected error in token decoding: {e}")
                return jsonify(message="An error occurred during token decoding.", error=str(e)), 500
        
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def role_required(allowed_roles):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                token = request.headers.get('Authorization')
                logging.info(f"Token received: {token}")
                if not token:
                    logging.warning("A valid token is missing")
                    return jsonify({'message': 'A valid token is missing'}), 403

                try:
                    # Correctly decode the token using the class's secret key and algorithm
                    token = token.split(" ")[1]  # Remove 'Bearer' prefix if present
                    decoded_token = jwt.decode(token, JWTService.secret_key, algorithms=[JWTService.algorithm])
                    logging.info(f"Decoded token: {decoded_token}")
                    user_role = decoded_token['role']
                    logging.info(f"User role from token: {user_role}")
                except jwt.ExpiredSignatureError:
                    logging.warning("Token expired")
                    return jsonify({'message': 'Token expired'}), 401
                except jwt.InvalidTokenError:
                    logging.warning("Invalid token")
                    return jsonify({'message': 'Invalid token'}), 401
                except Exception as e:
                    logging.error(f"Token validation error: {str(e)}")
                    return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 403

                if user_role not in allowed_roles:
                    logging.warning(f"Permission denied for role: {user_role}")
                    return jsonify({'message': 'Permission denied'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator