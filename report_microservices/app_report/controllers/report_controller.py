import os
import sys
def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()
import logging
import json
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from shared.auth_service import JWTService
from report_microservices.app_report.dto.complete_house_details_dto import CompleteHouseDetailsDTO
from report_microservices.app_report.dto.customer_report_dto import CustomerReportDTO
from report_microservices.app_report.dto.inspector_report_dto import InspectorReportDTO
from report_microservices.app_report.services.i_report_services import IReportService
from report_microservices.app_report.dto.building_component_dto import BuildingComponentDTO

from shared.custom_json_encoder import CustomJSONEncoder



def create_report_blueprint(report_service: IReportService):
    report_blueprint = Blueprint('reports', __name__, url_prefix='/api/reports')

    @report_blueprint.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy"}), 200
    
    
    @report_blueprint.route('/fetch_building_details', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def fetch_building_details():
        address = request.args.get('address')
        if not address:
            logging.error("Address is required")
            return jsonify({'error': 'Address is required'}), 400

        # Trim whitespace and newlines from the address
        address = address.strip()
        try:
            logging.info(f"Fetching building details for address: {address}")
            building_details = report_service.fetch_building_details(address)
            if building_details:
                logging.info(f"Building details fetched successfully for address: {address}")
                response_data = json.dumps(building_details.dict(), cls=CustomJSONEncoder)
                return response_data, 200, {'Content-Type': 'application/json'}
            else:
                logging.error(f"Failed to fetch building details for address: {address}")
                return jsonify({'error': 'Failed to fetch building details'}), 500
        except ValueError as e:
            logging.error(f"ValueError occurred: {str(e)}")
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            logging.error(f"Exception occurred while fetching building details: {str(e)}")
            return jsonify({'error': str(e)}), 500


    @report_blueprint.route('/generate_inspector_report', methods=['POST'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def generate_inspector_report():
        data = request.get_json()
        customer_report_id = data.get('customer_report_id')
        fetched_building_details_data = data.get('fetched_complete_house_details')

        if not customer_report_id or not fetched_building_details_data:
            logging.error("Customer report ID and building details are required")
            return jsonify({'error': 'Customer report ID and building details are required'}), 400

        try:
            logging.info(f"Generating inspector report for customer_report_id: {customer_report_id}")
            fetched_building_details = CompleteHouseDetailsDTO(**fetched_building_details_data)

            inspector_report_data = InspectorReportDTO(
                customer_report_id=customer_report_id,
                fetched_complete_house_details=fetched_building_details,
                discrepancies=data.get('discrepancies', ''),
                inspector_comments=data.get('inspector_comments', ''),
                inspection_date=data.get('inspection_date', ''),
                inspector_name=data.get('inspector_name', ''),
                inspector_signature=data.get('inspector_signature', ''),
                building_components=[BuildingComponentDTO(**comp) for comp in data.get('building_components', [])]
            )

            inspector_report = report_service.generate_inspector_report(inspector_report_data)

            if inspector_report:
                logging.info(f"Inspector report generated successfully for customer_report_id: {customer_report_id}")
                response_data = json.dumps(inspector_report.model_dump(), cls=CustomJSONEncoder)
                return response_data, 200, {'Content-Type': 'application/json'}
            else:
                logging.error(f"Failed to generate inspector report for customer_report_id: {customer_report_id}")
                return jsonify({'error': 'Failed to generate inspector report'}), 500
        except Exception as e:
            logging.error(f"Exception occurred while generating inspector report: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @report_blueprint.route('/create_combined_report/<customer_report_id>/<inspector_report_id>', methods=['POST'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def create_combined_report(customer_report_id, inspector_report_id):
        try:
            combined_report = report_service.create_combined_report(customer_report_id, inspector_report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        if not combined_report:
            return jsonify({"error": "Combined report could not be created"}), 404
        
        return jsonify(combined_report.dict())

    @report_blueprint.route('/get_inspector_report/<report_id>', methods=['GET'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_inspector_report(report_id):
        try:
            report = report_service.get_inspector_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        if not report:
            return jsonify({"error": "Inspector report not found"}), 404
        
        return jsonify(report.dict())

    @report_blueprint.route('/update_inspector_report/<report_id>', methods=['PUT'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def update_inspector_report(report_id):
        try:
            report_data = request.json
            updated_report = InspectorReportDTO(**report_data)
            report_service.update_inspector_report(report_id, updated_report)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Inspector report updated successfully"})

    @report_blueprint.route('/delete_inspector_report/<report_id>', methods=['DELETE'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def delete_inspector_report(report_id):
        try:
            report_service.delete_inspector_report(report_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return jsonify({"status": "Inspector report deleted successfully"})

    @report_blueprint.route('/submit_customer_report', methods=['POST'])
    @cross_origin(supports_credentials=True)
    @JWTService.token_required
    @JWTService.role_required(['CUSTOMER', 'INSPECTOR'])
    def submit_customer_report():
        try:
            data = request.json
            customer_report = CustomerReportDTO(**data)
            report_id = report_service.submit_customer_report(customer_report)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
        return jsonify({"status": "Customer report submitted successfully", "report_id": report_id})
    
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
