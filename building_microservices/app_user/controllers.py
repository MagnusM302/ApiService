from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import requests

app = Flask(__name__, template_folder='templates')

client = MongoClient("localhost", 27017)
db = client.mydatabase
people = db.people

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        address = request.form.get("address")
        return get_address(address)


@app.route('/users')
def get_users():
    people_found = list(people.find())

    for person in people_found:
        person['_id'] = str(person['_id'])

    people_json_str = dumps(people_found)
    people_data = loads(people_json_str)
    return render_template('people.html', people_list=people_data)


def get_address(address):
    response = requests.get('https://api.dataforsyningen.dk/navngivneveje', params={'q': address})

    if response.status_code == 200:
        address_details = response.json()
        return address_details
    else:
        return None


#headasd

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


