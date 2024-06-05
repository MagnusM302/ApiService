from flask import Flask, render_template, request, abort, jsonify
from pymongo import MongoClient
import requests
import logging
from enums import material_enums, building_enums

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

client = MongoClient("localhost", 27017)
db = client.mydatabase
people = db.people

username = 'XJCGPDGQSM'
password = '$Skole1234'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONTROLLERS
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        address = request.form.get("address")
        return get_address(address)

@app.route('/address_details/<string:id>', methods=['GET'])
def address_details(id):
    try:
        address_details, building_info = get_building_information(id)
        if address_details and building_info:
            return render_template('address_details.html', address_details=address_details, building_info=building_info, 
                                   material_enums=material_enums, building_enums=building_enums)
        else:
            logger.error("Invalid address ID or no building information found")
            return "Invalid address ID or no building information found", 400
    except ValueError:
        logger.error("Invalid address ID")
        return "Invalid address ID", 400

# BUSINESS LOGIC
def get_building_information(address_id):
    address_details = get_address_details(address_id)
    logger.info(f"Address details: {address_details}")
    
    if address_details and isinstance(address_details, list) and len(address_details) > 0:
        housenumber = address_details[0].get('husnummer', {}).get('id_lokalId')
        logger.info(f"Housenumber: {housenumber}")
        
        if housenumber:
            building_details = get_buildingbfe_from_housenumber(housenumber)
            logger.info(f"Building details: {building_details}")

            if building_details and 'gældendeJordstykke' in building_details:
                gældende_jordstykke = building_details['gældendeJordstykke']
                building_bfe = gældende_jordstykke.get('samletFastEjendom')
                
                if building_bfe:
                    ground_details = get_groundbfe_from_buildingbfe(building_bfe)
                    logger.info(f"Ground details: {ground_details}")
                    if ground_details and isinstance(ground_details, list) and len(ground_details) > 0:
                        ground_id = ground_details[0].get('id_lokalId')
                        logger.info(f"Ground ID: {ground_id}")
                        
                        if ground_id:
                            building_info = get_buildinginfo_from_groundid(ground_id)
                            logger.info(f"Building info: {building_info}")
                            
                            if building_info:
                                return address_details, building_info
                
    logger.error("Failed to retrieve building information")
    return None, None

# INFRASTRUCTURE
def get_address(address):
    response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address})

    if response.status_code == 200:
        address_details = response.json()
        return render_template('address.html', address_details=address_details, address=address)
    else:
        logger.error("Error retrieving address details")
        abort(400)

def get_address_details(address_id):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')

    if response.status_code == 200:
        address_details = response.json()
        logger.info(f"Address details: {address_details}")
        return address_details
    else:
        logger.error("Error retrieving address details")
        abort(400)

def get_housenumber_from_address(address_id):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresseTilHusnummer?username={username}&password={password}&Format=JSON&adresseId={address_id}')

    if response.status_code == 200:
        housenumber = response.json()
        logger.info(f"House number: {housenumber}")
        return housenumber
    else:  
        logger.error("Error retrieving house number")
        return None

def get_buildingbfe_from_housenumber(housenumber):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/husnummerTilJordstykke?HusnummerId={housenumber}')
    
    if response.status_code == 200:
        buildingbfe_details = response.json()
        logger.info(f"Building BFE details: {buildingbfe_details}")
        return buildingbfe_details
    else:
        logger.error("Error retrieving building BFE details")
        return None

def get_groundbfe_from_buildingbfe(buildingbfe):
    response = requests.get(f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/grund?username={username}&password={password}&Format=JSON&BFENummer={buildingbfe}')

    if response.status_code == 200:
        ground_details = response.json()
        logger.info(f"Ground details: {ground_details}")
        return ground_details
    else:
        logger.error("Error retrieving ground details")
        return None

def get_buildinginfo_from_groundid(groundid):
    response = requests.get(f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning?username={username}&password={password}&Format=JSON&Grund={groundid}')

    if response.status_code == 200:
        building_details = response.json()
        logger.info(f"Building details: {building_details}")
        return building_details
    else:
        logger.error("Error retrieving building details")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
