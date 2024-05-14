from flask import request, jsonify, make_response
from shared.json_utils import JsonUtils
from shared.auth_service import JWTService
from report_microservices.app_report.services import ReportService

def setup_routes(app, report_service):
    @app.route('/reports', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['Inspector'])
    def create_report():
        data = request.json
        report = report_service.create_report(data['property_details'], data['owner'])
        return jsonify(JsonUtils.convert_to_json_serializable(report)), 201

    @app.route('/reports/<report_id>', methods=['GET', 'PUT'])
    @JWTService.token_required
    @JWTService.role_required(['Customer', 'Inspector'])
    def manage_report(report_id):
        if request.method == 'GET':
            report = report_service.get_report(report_id)
            if report:
                return jsonify(JsonUtils.convert_to_json_serializable(report)), 200
            else:
                return jsonify({'error': 'Report not found'}), 404

        elif request.method == 'PUT':
            data = request.json
            report = report_service.update_report(report_id, data)
            if report:
                return jsonify({'message': 'Report updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update report'}), 404

    # Explicitly handle OPTIONS requests for CORS preflight
    @app.route('/reports', methods=['OPTIONS'])
    def handle_reports_options():
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    @app.route('/reports/<report_id>', methods=['OPTIONS'])
    def handle_report_id_options(report_id):
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

