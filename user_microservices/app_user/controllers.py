from flask import request, jsonify
from shared.auth_service import token_required, system_token_required, JWTService
from shared.json_utils import convert_to_json_serializable
from shared.config import ALLOWED_SERVICE_IDS

def setup_routes(app, user_service, jwt_service):
    jwt_service = JWTService(secret_key="your_secret_key_here")  # Antager at din hemmelige nøgle er konfigureret her

    @app.route('/system-token', methods=['POST'])
    def generate_system_token():
        service_id = request.json.get('service_id')
        if service_id in ALLOWED_SERVICE_IDS:
            token = jwt_service.generate_system_token(service_id)
            return jsonify({'system_token': token}), 200
        return jsonify({'error': 'Unauthorized service'}), 403

    @app.route('/protected-route')
    @token_required(jwt_service)
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
        user_dto = user_service.login_user(username, password)
        token = jwt_service.generate_token(user_dto.user_id, user_dto.role)
        return jsonify({'token': token, 'user_id': user_dto.user_id})

    @app.route('/users/<user_id>', methods=['GET'])
    @token_required(jwt_service)
    def get_user(user_id):
        user_dto = user_service.get_user(user_id)
        if user_dto:
            return jsonify(convert_to_json_serializable(user_dto)), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    @app.route('/users/<user_id>', methods=['PUT'])
    @token_required(jwt_service)
    def update_user(user_id):
        data = request.get_json()
        updated_user_dto = user_service.update_user(user_id, data)
        if updated_user_dto:
            return jsonify(convert_to_json_serializable(updated_user_dto)), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 404

    @app.route('/users/<user_id>', methods=['DELETE'])
    @token_required(jwt_service)
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            return jsonify({'message': 'User successfully deleted'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 404

    # Add more routes as needed
