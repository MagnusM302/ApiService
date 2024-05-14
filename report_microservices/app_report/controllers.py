from flask import request, jsonify
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

    @app.route('/reports/<report_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['Customer', 'Inspector'])
    def get_report(report_id):
        report = report_service.get_report(report_id)
        if report:
            return jsonify(JsonUtils.convert_to_json_serializable(report)), 200
        else:
            return jsonify({'error': 'Report not found'}), 404

    @app.route('/reports/<report_id>', methods=['PUT'])
    @JWTService.token_required
    @JWTService.role_required(['Inspector'])
    def update_report(report_id):
        data = request.json
        report = report_service.update_report(report_id, data)
        if report:
            return jsonify({'message': 'Report updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update report'}), 404
