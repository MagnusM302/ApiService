from flask import request, jsonify
from shared.auth_service import token_required, role_required
from shared.json_utils import convert_to_json_serializable

def setup_routes(app, report_service):
    @app.route('/reports', methods=['POST'])
    @token_required
    @role_required(['Inspector'])
    def create_report():
        data = request.json
        report = report_service.create_report(data['property_details'], data['owner'])
        return jsonify(convert_to_json_serializable(report)), 201

    @app.route('/reports/<report_id>', methods=['GET'])
    @token_required
    @role_required(['Customer', 'Inspector'])  # Allow access to both roles
    def get_report(report_id):
        report = report_service.get_report(report_id)
        if report:
            return jsonify(convert_to_json_serializable(report)), 200
        else:
            return jsonify({'error': 'Report not found'}), 404

    @app.route('/reports/<report_id>', methods=['PUT'])
    @token_required
    @role_required(['Inspector'])
    def update_report(report_id):
        data = request.json
        report = report_service.update_report(report_id, data)
        if report:
            return jsonify({'message': 'Report updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update report'}), 404
