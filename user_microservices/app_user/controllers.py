from flask import request, jsonify, make_response
from flask_cors import CORS  # Import CORS
from shared.auth_service import JWTService
from shared.json_utils import JsonUtils
from shared.config import ALLOWED_SERVICE_IDS
from user_microservices.app_user.services import UserService
from shared.routes import add_common_routes  # Import the common routes

def setup_routes(app, user_service):
    print("Setting up routes...")
    
    user_service = UserService()  # Assuming UserService doesn't need parameters for initialization

    @app.after_request
    def apply_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    @app.route('/register', methods=['POST'])
    @JWTService.token_required  # Use JWTService directly
    @JWTService.role_required(['Inspector'])
    def register():
        data = request.get_json()
        try:
            user_dto = user_service.register_user(**data)
            token = JWTService.generate_token(user_dto.user_id, user_dto.role)  # Use JWTService directly
            response = jsonify({'user_id': user_dto.user_id, 'token': token})
            return response, 201
        except ValueError as e:
            response = jsonify({'error': str(e)})
            return response, 400

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            response = jsonify({'error': 'Username and password are required'})
            return response, 400
        try:
            user_data = user_service.login_user(username, password)
            token = user_data['token']
            response = jsonify({'token': token, 'user_id': user_data['user_id'], 'role': user_data['role']})
            return response
        except ValueError as e:
            response = jsonify({'error': str(e)})
            return response, 401

    @app.route('/users/<user_id>', methods=['GET'])
    @JWTService.token_required
    def get_user(user_id):
        user_dto = user_service.get_user(user_id)
        if user_dto:
            response = jsonify(JsonUtils.convert_to_json_serializable(user_dto))
            return response
        else:
            response = jsonify({'error': 'User not found'})
            return response, 404

    @app.route('/users/<user_id>', methods=['PUT'])
    @JWTService.token_required
    def update_user(user_id):
        data = request.get_json()
        updated_user_dto = user_service.update_user(user_id, data)
        if updated_user_dto:
            response = jsonify(JsonUtils.convert_to_json_serializable(updated_user_dto))
            return response
        else:
            response = jsonify({'error': 'Failed to update user'})
            return response, 404

    @app.route('/users/<user_id>', methods=['DELETE'])
    @JWTService.token_required
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            response = jsonify({'message': 'User successfully deleted'})
            return response
        else:
            response = jsonify({'error': 'Failed to delete user'})
            return response, 404

    # Add common routes for system token generation and protected routes
    add_common_routes(app)
    
    # Add preflight route for CORS
    @app.route('/<path:path>', methods=['OPTIONS'])
    def preflight_handler(path):
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response
