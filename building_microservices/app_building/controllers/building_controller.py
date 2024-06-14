import os
import sys

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()

from flask import Blueprint, jsonify, request
from shared.json_utils import JsonUtils
from shared.auth_service import JWTService
from building_microservices.app_building.services.i_building_service import IBuildingService
from enum import Enum
import logging

def create_blueprint(building_service: IBuildingService):
    blueprint = Blueprint('app', __name__)

    @blueprint.route('/address', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_address():
        address = request.args.get('address')
        if not address:
            return jsonify({'error': 'Address parameter is required'}), 400
        try:
            address_dto = building_service.get_address(address)
            logging.info(f"Address DTO: {address_dto}")
            return jsonify(enum_to_value(address_dto.model_dump())), 200
        except Exception as e:
            logging.error(f"Error getting address: {e}")
            return jsonify({'error': str(e)}), 500

    @blueprint.route('/address/<string:address_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_address_details(address_id):
        try:
            address_dto = building_service.get_address_details(address_id)
            logging.info(f"Address Details DTO: {address_dto}")
            return jsonify(enum_to_value(address_dto.model_dump())), 200
        except Exception as e:
            logging.error(f"Error getting address details: {e}")
            return jsonify({'error': str(e)}), 500

    @blueprint.route('/building/<string:building_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_building_details(building_id):
        try:
            building_details_dto = building_service.get_building_details(building_id)
            logging.info(f"Building Details DTO: {building_details_dto}")
            # Convert enums before serialization
            building_details_data = enum_to_value(building_details_dto.model_dump())
            logging.info(f"Converted Building Details: {building_details_data}")
            return jsonify(building_details_data), 200
        except Exception as e:
            logging.error(f"Error getting building details: {e}")
            return jsonify({'error': str(e)}), 500
    
    @blueprint.route('/building/<string:building_id>/square_meters', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_building_square_meters(building_id):
        try:
            building_details_dto = building_service.get_building_details(building_id)
            square_meters_dto = {
                "id_lokalId": building_id,
                "samlet_bygningsareal": building_details_dto.byg038SamletBygningsareal,
                "samlede_boligareal": building_details_dto.byg039BygningensSamledeBoligAreal,
                "bebygget_areal": building_details_dto.byg041BebyggetAreal
            }
            logging.info(f"Square Meters DTO: {square_meters_dto}")
            return jsonify(enum_to_value(square_meters_dto)), 200
        except Exception as e:
            logging.error(f"Error getting building square meters: {e}")
            return jsonify({'error': str(e)}), 500
        
    return blueprint

def enum_to_value(data):
    if isinstance(data, dict):
        return {k: enum_to_value(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [enum_to_value(v) for v in data]
    elif isinstance(data, Enum):
        return data.value
    else:
        return data

# Ensure logging is configured
logging.basicConfig(level=logging.INFO)
