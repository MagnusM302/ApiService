# integration_test.py
import os
import sys

def add_project_to_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

add_project_to_sys_path()


import unittest
import requests
from multiprocessing import Process
from time import sleep
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from report_microservices.app_report.dto.customer_report_dto import CustomerReportDTO
from report_microservices.app_report.dto.inspector_report_dto import InspectorReportDTO
from report_microservices.app_report.dto.complete_house_details_dto import CompleteHouseDetailsDTO, OwnerDetailsDTO, HustypeDTO
from report_microservices.app_report.services.report_services import ReportService

USERNAME = "tryk12"
PASSWORD = "12345678"
ADDRESS = "kærvej 7, 9800"

logging.basicConfig(level=logging.INFO)


def run_user_service():
    from user_microservices.app_user.controller.user_controller import create_user_blueprint
    from user_microservices.app_user.dal.user_repository import UserRepository
    from user_microservices.app_user.services.user_service import UserService
    from shared.database import db_instance
    from shared.custom_dotenv import load_env_variables

    load_env_variables()

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    user_repository = UserRepository(db_instance)
    user_service = UserService(user_repository)
    user_blueprint = create_user_blueprint(user_service)
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def run_building_service():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

    mock_address_data = {"id": "unique-address-id", "status": 1, "darstatus": 3, "vejkode": "1946", "vejnavn": "Kærvej", "adresseringsvejnavn": "Kærvej", "husnr": "7", "etage": None, "dør": None, "supplerendebynavn": None, "postnr": "9800", "postnrnavn": "Hjørring", "stormodtagerpostnr": None, "stormodtagerpostnrnavn": None, "kommunekode": "0860", "adgangsadresseid": "0a3f509a-828f-32b8-e044-0003ba298018", "x": 9.9904539, "y": 57.45180085, "href": "https://api.dataforsyningen.dk/adresser/0a3f50c8-2902-32b8-e044-0003ba298018"}

    mock_building_data = {"id": "unique-building-id", "building_name": "Test Building", "address_id": "0a3f509a-828f-32b8-e044-0003ba298018", "construction_year": 2000, "number_of_floors": 5}

    @app.route('/api/buildings/address', methods=['GET'])
    def get_address():
        address = request.args.get('address')
        if address == ADDRESS:
            return jsonify(mock_address_data), 200
        return jsonify([]), 404

    @app.route('/api/buildings/building/<building_id>', methods=['GET'])
    def get_building(building_id):
        if building_id == mock_building_data["id"]:
            return jsonify(mock_building_data), 200
        return jsonify({"error": "No building data found"}), 404

    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)

def run_report_service(token):
    from report_microservices.app_report.dal.report_repository import ReportRepository
    from report_microservices.app_report.controllers import create_report_blueprint
    from report_microservices.app_report.client.building_service_client import BuildingServiceClient
    from shared.custom_dotenv import load_env_variables
    from shared.database import db_instance

    load_env_variables()

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api", token=token)
    report_repository = ReportRepository(db_instance)
    report_service = ReportService(building_service_client, report_repository)
    report_blueprint = create_report_blueprint(report_service)
    app.register_blueprint(report_blueprint, url_prefix='/api/reports')
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

class TestReportService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_service_process = Process(target=run_user_service)
        cls.building_service_process = Process(target=run_building_service)

        cls.user_service_process.start()
        cls.building_service_process.start()

        sleep(40)

        login_url = "http://localhost:5000/api/users/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        login_response = requests.post(login_url, json=login_data)
        cls.token = login_response.json()["token"]

        cls.report_service_process = Process(target=run_report_service, args=(cls.token,))
        cls.report_service_process.start()
        sleep(30)

        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    @classmethod
    def tearDownClass(cls):
        cls.user_service_process.terminate()
        cls.building_service_process.terminate()
        cls.report_service_process.terminate()

    def test_submit_customer_report(self):
        customer_report_data = CustomerReportDTO(
            name="Test Customer",
            phone="1234567890",
            email="test@example.com",
            address=ADDRESS,
            bestilling_oplysninger="Bestilling oplysninger",
            ejendomsmægler="Ejendomsmægler",
            ejer_år="5",
            boet_periode="5 år",
            tilbygninger="Ingen tilbygninger",
            ombygninger="Ingen ombygninger",
            renoveringer="Ingen renoveringer",
            andre_bygninger="Ingen andre bygninger",
            tag="God stand",
            ydermur="God stand",
            indre_vægge="God stand",
            fundamenter="God stand",
            kælder="Ingen kælder",
            gulve="God stand",
            vinduer_døre="God stand",
            lofter_etageadskillelser="God stand",
            vådrum="God stand",
            vvs="God stand"
        )

        response = requests.post("http://localhost:5006/api/reports/submit_customer_report", json=customer_report_data.dict(), headers=self.headers)
        
        self.assertEqual(response.status_code, 200, f"Failed to submit customer report: {response.json()}")
        self.customer_report_id = response.json()["report_id"]

    def test_generate_inspector_report(self):
        self.test_submit_customer_report()  # Sikrer, at vi har en customer_report_id

        customer_report_id = self.customer_report_id

        building_details = {
            "id": "64b3b9f8c6abf7a0d2f9b8c1",
            "address": "kærvej 7, 9800",
            "year_built": "1990",
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com",
                "period_of_ownership": "10 years",
                "construction_knowledge": "Expert"
            },
            "hustype": {
                "description": "Villa",
                "type_id": "1"
            },
            "basement_present": True,
            "building_components": [],
            "varmeinstallation": "1",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "No remarks"
        }

        complete_house_details_dto = CompleteHouseDetailsDTO(**building_details)

        inspector_report_data = {
            "customer_report_id": customer_report_id,
            "fetched_complete_house_details": complete_house_details_dto.model_dump(),  # Brug model_dump()
            "discrepancies": "None",
            "inspector_comments": "All good",
            "inspection_date": "2024-06-17",
            "inspector_name": "Inspector Gadget",
            "inspector_signature": "Inspector Gadget",
            "building_components": []  # Tilføj relevante komponenter her
        }

    # Debug-udskrifter for at verificere dataene
        print("Customer Report ID:", customer_report_id)
        print("Building Details:", building_details)
        print("Inspector Report Data:", inspector_report_data)

        response = requests.post("http://localhost:5006/api/reports/generate_inspector_report", json=inspector_report_data, headers=self.headers)

    # Udskrift af response status og indhold
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.json())

        self.assertEqual(response.status_code, 200, f"Failed to generate inspector report: {response.json()}")

if __name__ == '__main__':
    unittest.main()
