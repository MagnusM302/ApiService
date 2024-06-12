from flask import Blueprint, jsonify, request
from shared.auth_service import JWTService
from app_report.dto.complete_house_details_dto import CompleteHouseDetailsDTO
from app_report.dto.customer_report_dto import CustomerReportDTO
from app_report.services.iservices import IReportService

def create_blueprint(report_service: IReportService):
    blueprint = Blueprint('reports', __name__)

    @blueprint.route('/generate_report', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def generate_report():
        data = request.json
        address = data.get('address')
        
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        try:
            report = report_service.generate_report(address)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        if not report:
            return jsonify({"error": "Report could not be generated"}), 404
        
        return jsonify(report.model_dump())

    @blueprint.route('/get_report/<report_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_report(report_id):
        try:
            report = report_service.get_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        return jsonify(report.model_dump())

    @blueprint.route('/update_report/<report_id>', methods=['PUT'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def update_report(report_id):
        try:
            report_data = request.json
            updated_report = CompleteHouseDetailsDTO(**report_data)
            report_service.update_report(report_id, updated_report)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Report updated successfully"})

    @blueprint.route('/delete_report/<report_id>', methods=['DELETE'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def delete_report(report_id):
        try:
            report_service.delete_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Report deleted successfully"})

    @blueprint.route('/submit_customer_report', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['CUSTOMER'])
    def submit_customer_report():
        try:
            data = request.json
            customer_report = CustomerReportDTO(**data)
            report_id = report_service.submit_customer_report(customer_report)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Customer report submitted successfully", "report_id": report_id})

    @blueprint.route('/create_complete_report/<customer_report_id>', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def create_complete_report(customer_report_id):
        try:
            complete_report = report_service.create_complete_report(customer_report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        if not complete_report:
            return jsonify({"error": "Complete report could not be created"}), 404
        
        return jsonify(complete_report.model_dump())

    @blueprint.route('/delete_customer_report/<report_id>', methods=['DELETE'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def delete_customer_report(report_id):
        try:
            report_service.delete_customer_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Customer report deleted successfully"})

    return blueprint
