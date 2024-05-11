import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import request, jsonify
from shared.auth_service import JWTService
from shared.json_utils import JsonUtils
from shared.config import ALLOWED_SERVICE_IDS
from .services import UserService

def setup_routes(app, user_service, jwt_service):
    jwt_service = JWTService(secret_key="your_secret_key_here")  # Antager at din hemmelige nøgle er konfigureret her
    user_service = UserService() 
    
    @app.route('/system-token', methods=['POST'])
    def generate_system_token():
        service_id = request.json.get('service_id')
        if service_id in ALLOWED_SERVICE_IDS:
            token = jwt_service.generate_system_token(service_id)
            return jsonify({'system_token': token}), 200
        return jsonify({'error': 'Unauthorized service'}), 403

    @app.route('/protected-route')
    @jwt_service.token_required
    def protected_route():
        return "This is a protected area!"

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        user_dto = user_service.register_user(**data)
        token = jwt_service.generate_token(user_dto.user_id, user_dto.role)
        return jsonify({'user_id': user_dto.user_id, 'token': token}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return jsonify({'error': 'Username and password are required'}), 400
        try:
            user_dto = user_service.login_user(username, password)
            token = jwt_service.generate_token(user_dto['user_id'], user_dto['role'])
            return jsonify({'token': token, 'user_id': user_dto['user_id']})
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except KeyError as e:
            return jsonify({'error': 'Missing key in user data: {}'.format(e)}), 500



    @app.route('/users/<user_id>', methods=['GET'])
    @jwt_service.token_required
    def get_user(user_id):
        user_dto = user_service.get_user(user_id)
        if user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(user_dto)), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    @app.route('/users/<user_id>', methods=['PUT'])
    @jwt_service.token_required
    def update_user(user_id):
        data = request.get_json()
        updated_user_dto = user_service.update_user(user_id, data)
        if updated_user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(updated_user_dto)), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 404

    @app.route('/users/<user_id>', methods=['DELETE'])
    @jwt_service.token_required
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            return jsonify({'message': 'User successfully deleted'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 404

    # Add more routes as needed
