import sys
import os
import unittest
import requests
from multiprocessing import Process
from time import sleep
from pymongo import MongoClient
import bcrypt
from enum import Enum

def add_project_to_sys_path():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app_report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app_report'))
    if root_path not in sys.path:
        sys.path.append(root_path)
    if app_report_path not in sys.path:
        sys.path.append(app_report_path)

def run_user_service():
    add_project_to_sys_path()
    from user_microservices.run import create_user_app
    app = create_user_app()
    app.run(port=5001, debug=True, use_reloader=False)

def run_building_service():
    add_project_to_sys_path()
    from building_microservices.run import create_building_app
    app = create_building_app()
    app.run(port=5005, debug=True, use_reloader=False)

def run_report_service():
    add_project_to_sys_path()
    from report_microservices.run import create_app
    app = create_app()
    app.run(port=5006, debug=True, use_reloader=False)

USER_SERVICE_URL = "http://localhost:5001"
BUILDING_SERVICE_URL = "http://localhost:5005"
REPORT_SERVICE_URL = "http://localhost:5006"

USERNAME = "tryk12"
PASSWORD = "12345678"
ADDRESS = "kærvej 7, 9800"

class UserRole(Enum):
    INSPECTOR = 1
    CUSTOMER = 2

class TestReportService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_service_process = Process(target=run_user_service)
        cls.building_service_process = Process(target=run_building_service)
        cls.report_service_process = Process(target=run_report_service)
        
        cls.user_service_process.start()
        cls.building_service_process.start()
        cls.report_service_process.start()
        
        sleep(40)  # Give the services more time to start

        cls.client = MongoClient('mongodb+srv://buildingDBuser:$Skole1234@cluster0.dezwb5i.mongodb.net/BuildingReportsDB?retryWrites=true&w=majority')
        cls.db = cls.client['BuildingReportsDB']
        cls.users_collection = cls.db['users']
        cls.buildings_collection = cls.db['buildings']
        cls.addresses_collection = cls.db['addresses']

        cls.inspector_credentials = {
            "username": USERNAME,
            "password": PASSWORD
        }
        cls.inspector_details = {
            "name": "Inspector User",
            "address": "123 Inspector St",
            "post_number": "1234",
            "phone": "12345678",
            "username": cls.inspector_credentials['username'],
            "email": "inspector@example.com",
            "role": UserRole.INSPECTOR.value,
            "password_hash": bcrypt.hashpw(cls.inspector_credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }
        if cls.users_collection.find_one({"username": cls.inspector_credentials['username']}) is None:
            cls.users_collection.insert_one(cls.inspector_details)

        login_url = f"{USER_SERVICE_URL}/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        for i in range(5):
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                break
            sleep(5)
        assert response.status_code == 200, f"Login failed: {response.json()}"
        cls.token = response.json()['token']
        print(f"Token: {cls.token}")

        # Configure the BuildingServiceClient with the obtained token
        add_project_to_sys_path()  # Ensure the app_report path is added to sys.path
        from report_microservices.app_report.client.building_service_client import BuildingServiceClient
        cls.building_service_client = BuildingServiceClient(token=cls.token)

    @classmethod
    def tearDownClass(cls):
        cls.buildings_collection.delete_many({"id": "3d90f674-e642-4516-b4a1-45f2617b561f"})
        cls.addresses_collection.delete_many({"id": "0a3f50c8-2902-32b8-e044-0003ba298018"})
        
        cls.user_service_process.terminate()
        cls.user_service_process.join()
        
        cls.building_service_process.terminate()
        cls.building_service_process.join()

        cls.report_service_process.terminate()
        cls.report_service_process.join()

    def test_generate_report(self):
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"

        # Create test data for building service
        building_data = {
            "id": building_id,
            "byg007Bygningsnummer": "1",
            "byg021BygningensAnvendelse": "120",
            "byg056Varmeinstallation": "1",
            "byg032YdervæggensMateriale": "1",
            "byg033Tagdækningsmateriale": "3",
            "byg037KildeTilBygningensMaterialer": "1",
            "byg058SupplerendeVarme": "5",
            "byg026Opførelsesår": 1952,
            "byg038SamletBygningsareal": 139,
            "byg039BygningensSamledeBoligAreal": 139,
            "byg041BebyggetAreal": 139,
            "byg053BygningsarealerKilde": "1",
            "byg054AntalEtager": 1,
            "byg094Revisionsdato": "2017-09-24T09:13:32.432586+02:00",
            "byg133KildeTilKoordinatsæt": "K",
            "byg134KvalitetAfKoordinatsæt": "1",
            "byg135SupplerendeOplysningOmKoordinatsæt": "11",
            "byg136PlaceringPåSøterritorie": "0",
            "byg404Koordinat": "POINT(559435.67 6368107.12)",
            "byg406Koordinatsystem": "5",
            "forretningshændelse": "Bygning",
            "forretningsområde": "54.15.05.05",
            "forretningsproces": "25",
            "grund": "8bd15ce3-07be-4ec1-bd7a-c68b5917ca10",
            "husnummer": "0a3f509a-828f-32b8-e044-0003ba298018",
            "jordstykke": "1372860",
            "kommunekode": "0860",
            "registreringFra": "2017-09-24T09:13:32.432586+02:00",
            "registreringsaktør": "BBR",
            "status": "6",
            "virkningFra": "2017-09-24T09:13:32.432586+02:00",
            "virkningsaktør": "EksterntSystem",
            "etageList": [],
            "opgangList": []
        }

        address_data = {
            "id": address_id,
            "vejkode": "1946",
            "vejnavn": "Kærvej",
            "adresseringsvejnavn": "Kærvej",
            "husnr": "7",
            "postnr": "9800",
            "postnrnavn": "Hjørring",
            "kommunekode": "0860",
            "adgangsadresseid": "0a3f509a-828f-32b8-e044-0003ba298018",
            "x": 9.9904539,
            "y": 57.45180085,
            "href": "https://api.dataforsyningen.dk/adresser/0a3f50c8-2902-32b8-e044-0003ba298018",
            "status": 1,
            "darstatus": 3,
            "tekst": "Kærvej 7, 9800 Hjørring"
        }

        # Insert test data into building service database
        buildings_collection = self.db['buildings']
        addresses_collection = self.db['addresses']

        buildings_collection.insert_one(building_data)
        addresses_collection.insert_one(address_data)

        # Verify insertion
        inserted_building = buildings_collection.find_one({"id": building_id})
        inserted_address = addresses_collection.find_one({"id": address_id})
        print(f"Inserted building: {inserted_building}")
        print(f"Inserted address: {inserted_address}")

        assert inserted_building is not None, "Building data not inserted correctly"
        assert inserted_address is not None, "Address data not inserted correctly"

        # Call the report service to generate a report
        generate_report_url = f"{REPORT_SERVICE_URL}/api/reports/generate_report"
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'building_id': building_id, 'address_id': address_id}

        # Sleep to ensure the services have time to sync
        sleep(10)

        response = requests.get(generate_report_url, headers=headers, params=params)
        self.assertEqual(response.status_code, 200, f"Failed to generate report: {response.json()}")
        report = response.json()
        self.assertEqual(report['year_built'], 1952)
        self.assertEqual(report['address'], "Kærvej 7, 9800 Hjørring")

        # Clean up the inserted data
        buildings_collection.delete_one({"id": building_id})
        addresses_collection.delete_one({"id": address_id})

if __name__ == '__main__':
    unittest.main()
