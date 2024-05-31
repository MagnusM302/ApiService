from flask import Blueprint, request, jsonify
from app_building.services import BuildingService
from dtos.dto_converters import DTOConverters
import logging

controller = Blueprint('controller', __name__)

@controller.route('/api/get_address', methods=['GET'])
def get_address():
    address = request.args.get('address')
    try:
        address_dto = BuildingService.get_address(address)
        return jsonify(address_dto.dict())
    except Exception as e:
        logging.error(f'Failed to fetch address details: {e}')
        return jsonify({'error': str(e)}), 500

@controller.route('/api/get_address_details', methods=['GET'])
def get_address_details():
    address_id = request.args.get('address_id')
    try:
        address_details = BuildingService.get_address_details(address_id)
        return jsonify(address_details)
    except Exception as e:
        logging.error(f'Failed to fetch address details: {e}')
        return jsonify({'error': str(e)}), 500

@controller.route('/api/get_building_details', methods=['GET'])
def get_building_details():
    building_id = request.args.get('building_id')  # Parameter to reflect building_id
    try:
        building_details_dto = BuildingService.get_building_details(building_id)
        return jsonify(building_details_dto.dict())
    except Exception as e:
        logging.error(f'Failed to fetch building details: {e}')
        return jsonify({'error': str(e)}), 500

@controller.route('/api/full_details', methods=['GET'])
def full_details():
    address = request.args.get('address')
    try:
        complete_house_details_dto = BuildingService.get_complete_house_details(address)
        return jsonify(complete_house_details_dto.dict())
    except Exception as e:
        logging.error(f'Failed to fetch full details: {e}')
        return jsonify({'error': str(e)}), 500

