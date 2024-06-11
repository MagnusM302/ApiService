from flask import Blueprint, request, jsonify
from shared.auth_service import JWTService
from shared.json_utils import JsonUtils
from shared.config import ALLOWED_SERVICE_IDS
from user_microservices.app_user.services import UserService

user_blueprint = Blueprint('user', __name__)

def setup_routes(user_service):
    @user_blueprint.route('/system-token', methods=['POST'])
    def generate_system_token():
        service_id = request.json.get('service_id')
        if service_id in ALLOWED_SERVICE_IDS:
            token = JWTService.generate_system_token(service_id)
            return jsonify({'system_token': token}), 200
        return jsonify({'error': 'Unauthorized service'}), 403

    @user_blueprint.route('/protected-route')
    @JWTService.token_required
    def protected_route():
        return "This is a protected area!"

    @user_blueprint.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        user_dto = user_service.register_user(**data)
        token = JWTService.generate_token(user_dto.user_id, user_dto.role)
        return jsonify({'user_id': user_dto.user_id, 'token': token}), 201

    @user_blueprint.route('/login', methods=['POST'])
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
    @JWTService.token_required
    def get_user(user_id):
        user_dto = user_service.get_user(user_id)
        if user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(user_dto)), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    @user_blueprint.route('/users/<user_id>', methods=['PUT'])
    @JWTService.token_required
    def update_user(user_id):
        data = request.get_json()
        updated_user_dto = user_service.update_user(user_id, data)
        if updated_user_dto:
            return jsonify(JsonUtils.convert_to_json_serializable(updated_user_dto)), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 404

    @user_blueprint.route('/users/<user_id>', methods=['DELETE'])
    @JWTService.token_required
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            return jsonify({'message': 'User successfully deleted'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 404


# This function should be called to register the routes
def register_user_routes(app):
    user_service = UserService()  # Assuming UserService doesn't need parameters for initialization
    setup_routes(user_service)
    app.register_blueprint(user_blueprint)