# user_microservices/app_user/controllers.py
from flask import request, jsonify, make_response
from flask_cors import CORS
from shared.auth_service import JWTService
from user_microservices.app_user.services import UserService
from shared.routes import add_common_routes

def setup_routes(app, user_service):
    print("Setting up routes...")
    
    user_service = UserService()

    @app.after_request
    def apply_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    @app.route('/register', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['Inspector'])
    def register():
        data = request.get_json()
        try:
            user_dto = user_service.register_user(**data)
            token = JWTService.generate_token(user_dto.user_id, user_dto.role)
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

    add_common_routes(app)
    
    @app.route('/<path:path>', methods=['OPTIONS'])
    def preflight_handler(path):
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response
