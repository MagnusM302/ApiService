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
from flask import Blueprint, jsonify, request
from enum import Enum
from building_microservices.app_building.services.i_building_service import IBuildingService

# Ensure logging is configured
logging.basicConfig(level=logging.INFO)


def create_building_blueprint(building_service: IBuildingService):
    building_blueprint = Blueprint('buildings', __name__, url_prefix='/api/buildings')

    @building_blueprint.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy"}), 200

    @building_blueprint.route('/address', methods=['GET'])
    def get_address():
        address = request.args.get('address')
        if not address:
            return jsonify({'error': 'Address parameter is required'}), 400
        try:
            address_dto = building_service.get_address(address)
            logging.info(f"Address DTO: {address_dto}")
            return jsonify(enum_to_value(address_dto.dict())), 200
        except Exception as e:
            logging.error(f"Error getting address: {e}")
            return jsonify({'error': str(e)}), 500

    @building_blueprint.route('/address/<string:address_id>', methods=['GET'])
    def get_address_details(address_id):
        try:
            address_dto = building_service.get_address_details(address_id)
            logging.info(f"Address Details DTO: {address_dto}")
            return jsonify(enum_to_value(address_dto.model_dump())), 200
        except Exception as e:
            logging.error(f"Error getting address details: {e}")
            return jsonify({'error': str(e)}), 500

    @building_blueprint.route('/building/<string:building_id>', methods=['GET'])
    def get_building_details(building_id):
        try:
            building_details_dto = building_service.get_building_details(building_id)
            logging.info(f"Building Details DTO: {building_details_dto}")
            # Convert enums before serialization
            building_details_data = enum_to_value(building_details_dto.dict())
            logging.info(f"Converted Building Details: {building_details_data}")
            return jsonify(building_details_data), 200
        except Exception as e:
            logging.error(f"Error getting building details: {e}")
            return jsonify({'error': str(e)}), 500

    @building_blueprint.route('/complete_building_details', methods=['GET'])
    def fetch_complete_building_details():
        address = request.args.get('address')
        if not address:
            return jsonify({'error': 'Address parameter is required'}), 400
        try:
            complete_building_details_dto = building_service.fetch_complete_building_details(address)
            logging.info(f"Complete Building Details DTO: {complete_building_details_dto}")
            return jsonify(enum_to_value(complete_building_details_dto.dict())), 200
        except Exception as e:
            logging.error(f"Error fetching complete building details: {e}")
            return jsonify({'error': str(e)}), 500

    return building_blueprint

def enum_to_value(data):
    if isinstance(data, dict):
        return {k: enum_to_value(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [enum_to_value(v) for v in data]
    elif isinstance(data, Enum):
        return data.value
    else:
        return data