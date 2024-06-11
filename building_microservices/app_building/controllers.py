from flask import Blueprint, jsonify, request
from shared.json_utils import JsonUtils
from shared.auth_service import JWTService
from app_building.services.interfaces import IBuildingService

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
            return jsonify(address_dto.dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @blueprint.route('/address/<string:address_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_address_details(address_id):
        try:
            address_dto = building_service.get_address_details(address_id)
            return jsonify(address_dto.dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @blueprint.route('/building/<string:building_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['INSPECTOR'])
    def get_building_details(building_id):
        try:
            building_details_dto = building_service.get_building_details(building_id)
            return jsonify(building_details_dto.dict()), 200
        except Exception as e:
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
            return jsonify(square_meters_dto), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return blueprint
