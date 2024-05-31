from flask import Flask, jsonify, request, abort
from .auth_service import JWTService
from .config import ALLOWED_SERVICE_IDS
from flask_cors import CORS
import logging


def add_common_routes(app):
    CORS(app , resources={r"/*": {"origins": "*"}})
    @app.route('/system-token', methods=['POST'])
    def generate_system_token():
        service_id = request.json.get('service_id')
        if service_id in ALLOWED_SERVICE_IDS:
            token = JWTService.generate_system_token(service_id)
            return jsonify({'system_token': token}), 200
        return jsonify({'error': 'Unauthorized service'}), 403

    @app.route('/protected-route')
    @JWTService.token_required
    def protected_route():
        return "This is a protected area!"

    @app.errorhandler(401)
    def unauthorized(error=None):
        message = {
            'status': 401,
            'message': 'Unauthorized: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 401
        return resp
    