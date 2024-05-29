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



#INFRASTRUCTURE
def get_address(address):
    response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address})

    if response.status_code == 200:
        address_details = response.json()
        return render_template('address.html', address_details=address_details, address=address)
    else:
        abort(400)

def get_address_details(address_id):
    print('We got to here! ' + address_id) 
    response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')

    if response.status_code == 200:
        address_details = response.json()
        print(address_details)
        return address_details
    else:
        abort(400)

def get_housenumber_from_address(address_id):
    return ""

def get_buildingbfe_from_housenumber(housenumber):
    return ""

def get_groundbfe_from_buildingbfe(buildingbfe):
    return ""

def get_buildinginfo_from_groundid(groundbfe):
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
