from flask import Flask, render_template, request, abort, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import requests

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

client = MongoClient("localhost", 27017)
db = client.mydatabase
people = db.people

username = 'XJCGPDGQSM'
password = '$Skole1234'

#CONTROLLERS
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
        address_details = get_address_details(id)
        return render_template('address_details.html', address_details=address_details)
    except ValueError:
        return "Invalid address ID", 400


#BUSINESSLOGIC
def get_building_information(address_id):
    return ""


#INFRASTRUCTURE
def get_address(address):
    response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address})

    if response.status_code == 200:
        address_details = response.json()
        return render_template('address.html', address_details=address_details, address=address)
    else:
        abort(400)

def get_address_details(address_id):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')

    if response.status_code == 200:
        address_details = response.json()
        print(address_details)
        return address_details
    else:
        abort(400)

def get_housenumber_from_address(address_id):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresseTilHusnummer?username={username}&password={password}&Format=JSON&adresseId={address_id}')

    if response.status_code == 200:
        housenumber = response.json()
        print(housenumber)
        return housenumber
    else:  
        return "Something went wrong retrieving the house number", 400


def get_buildingbfe_from_housenumber(housenumber):
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/husnummerTilJordstykke?HusnummerId={housenumber}')
    
    if response.status_code == 200:
        buildingbfe_details = response.json()
        print(buildingbfe_details)
        return buildingbfe_details
    else:
        return "Something went wrong retrieving the building details", 400

def get_groundbfe_from_buildingbfe(buildingbfe):
    response = requests.get(f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/grund?username={username}&password={password}&Format=JSON&BFENummer={buildingbfe}')

    if response.status_code == 200:
        ground_details = response.json()
        print(ground_details)
        return ground_details
    else:
        return "Something went wrong retrieving the ground details", 400

def get_buildinginfo_from_groundid(groundid):
    response = requests.get(f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning?username={username}&password={password}&Format=JSON&Grund={groundid}')

    if response.status_code == 200:
        building_details = response.json()
        print(building_details)
        return building_details
    else:
        return "Something went wrong retrieving the building details", 400
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
