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
from report_microservices.app_report.dto.complete_house_details_dto import CompleteHouseDetailsDTO
from report_microservices.app_report.dto.customer_report_dto import CustomerReportDTO
from report_microservices.app_report.services.i_report_services import IReportService

def create_report_blueprint(report_service: IReportService):
    report_blueprint = Blueprint('reports', __name__)

    @report_blueprint.route('/generate_report', methods=['POST'], endpoint='generate_report')
    @cross_origin(supports_credentials=True)
    def generate_report():
        data = request.get_json()
        address = data.get('address')
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        try:
            report = report_service.generate_report(address)
            if report:
                return jsonify(report), 200
            else:
                return jsonify({'error': 'Failed to generate report'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @report_blueprint.route('/get_report/<report_id>', methods=['GET'])
    @cross_origin(supports_credentials=True)
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

    @report_blueprint.route('/update_report/<report_id>', methods=['PUT'])
    @cross_origin(supports_credentials=True)
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

    @report_blueprint.route('/delete_report/<report_id>', methods=['DELETE'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def delete_report(report_id):
        try:
            report_service.delete_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Report deleted successfully"})

    @report_blueprint.route('/submit_customer_report', methods=['POST'])
    @cross_origin(supports_credentials=True)
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

    @report_blueprint.route('/create_complete_report/<customer_report_id>', methods=['POST'])
    @cross_origin(supports_credentials=True)
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

    @report_blueprint.route('/delete_customer_report/<report_id>', methods=['DELETE'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def delete_customer_report(report_id):
        try:
            report_service.delete_customer_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Customer report deleted successfully"})

    return report_blueprint
