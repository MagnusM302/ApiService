import os
import sys

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from shared.auth_service import JWTService
from shared.config import ALLOWED_SERVICE_IDS
from shared.json_utils import JsonUtils
from user_microservices.app_user.services.i_user_service import IUserService

def create_user_blueprint(user_service: IUserService):
    user_blueprint = Blueprint('user', __name__)

    @user_blueprint.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    @user_blueprint.route('/system-token', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def generate_system_token():
        print(f"Received request with method: {request.method}")
        print(f"Request JSON: {request.json}")
        service_id = request.json.get('service_id')
        if service_id in ALLOWED_SERVICE_IDS:
            token = JWTService.generate_system_token(service_id)
            return jsonify({'system_token': token}), 200
        return jsonify({'error': 'Unauthorized service'}), 403
    
    @user_blueprint.route('/protected-route')
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    def protected_route():
        return "This is a protected area!"

    @user_blueprint.route('/register', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def register():
        data = request.get_json()
        user_dto = user_service.register_user(**data)
        token = JWTService.generate_token(user_dto.user_id, user_dto.role)
        return jsonify({'user_id': user_dto.user_id, 'token': token}), 201

    @user_blueprint.route('/login', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return jsonify({'error': 'Username and password are required'}), 400
        try:
            user_dto = user_service.login_user(username, password)
            return jsonify({'token': user_dto['token'], 'user_id': user_dto['user_id'], 'role': user_dto['role']})
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except KeyError as e:
            return jsonify({'error': 'Missing key in user data: {}'.format(e)}), 500

    @user_blueprint.route('/users/<user_id>', methods=['GET'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    def get_user(user_id):
        user_dto = user_service.get_user(user_id)
        if user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(user_dto)), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    @user_blueprint.route('/users/<user_id>', methods=['PUT'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    def update_user(user_id):
        data = request.get_json()
        updated_user_dto = user_service.update_user(user_id, data)
        if updated_user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(updated_user_dto)), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 404

    @user_blueprint.route('/users/<user_id>', methods=['DELETE'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            return jsonify({'message': 'User successfully deleted'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 404

    return user_blueprint