from flask import Blueprint, request, jsonify
import requests
import logging

controller = Blueprint('controller', __name__)

@controller.route('/api/get_address', methods=['GET'])
def get_address():
    address = request.args.get('address')
    response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address, 'type': 'adresse'})
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch address details'}), 500

@controller.route('/api/get_address_details', methods=['GET'])
def get_address_details():
    address_id = request.args.get('address_id')
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch address details'}), 500

@controller.route('/api/get_building_details', methods=['GET'])
def get_building_details():
    building_id = request.args.get('address_id')  # Parameter to reflect building_id
    username = "XJCGPDGQSM"  # Replace with your username
    password = "$Skole1234"  # Replace with your password
    params = {
        'id': building_id,
        'username': username,
        'password': password,
    }

    logging.info(f'Requesting building details with params: {params}')

    response = requests.get('https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning', params=params)
    
    logging.info(f'API response status code: {response.status_code}')
    logging.info(f'API response: {response.text}')
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            return jsonify(data[0])  # Ensure it returns a single dictionary
        else:
            logging.error('Building details list is empty or incorrect format')
            return jsonify({'error': 'Building details list is empty or incorrect format'}), 500
    else:
        logging.error(f'Failed to fetch building details. Status code: {response.status_code}, Response: {response.text}')
        return jsonify({'error': 'Failed to fetch building details'}), 500

@controller.route('/api/full_details', methods=['GET'])
def full_details():
    address = request.args.get('address')
    # Fetch address ID
    address_response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address, 'type': 'adresse'})
    
    if address_response.status_code == 200:
        address_data = address_response.json()
        if not address_data:
            return jsonify({'error': 'No address data found'}), 404

        # Assuming the first result is the relevant one
        address_id = address_data[0]['data']['id']  # Adjust the key based on actual response structure

        # Fetch address details
        details_response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')
        
        if details_response.status_code == 200:
            address_details = details_response.json()
            
            # Extract building ID from address details
            building_id = address_details[0]['husnummer']['adgangTilBygning']
            
            # Fetch building details
            username = "XJCGPDGQSM"  # Replace with your username
            password = "$Skole1234"  # Replace with your password
            params = {
                'id': building_id,
                'username': username,
                'password': password,
            }
            
            building_response = requests.get('https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning', params=params)
            
            if building_response.status_code == 200:
                building_details = building_response.json()
                return jsonify({
                    'address_details': address_details,
                    'building_details': building_details[0]  # Ensure it returns a single dictionary
                })
            else:
                return jsonify({'error': 'Failed to fetch building details'}), 500
        else:
            return jsonify({'error': 'Failed to fetch address details'}), 500
    else:
        return jsonify({'error': 'Failed to fetch address details'}), 500
