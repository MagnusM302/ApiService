import sys
import os
import unittest
import requests
from multiprocessing import Process
from time import sleep
from bson import ObjectId
from enum import Enum

def add_project_to_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

add_project_to_sys_path()

# Import necessary modules
from report_microservices.app_report.services.report_services import ReportService
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from report_microservices.app_report.dto.inspector_report_dto import InspectorReportDTO
from report_microservices.app_report.dto.customer_report_dto import CustomerReportDTO
from report_microservices.app_report.dto.complete_house_details_dto import CompleteHouseDetailsDTO
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from shared.database import db_instance

def run_user_service():
    from flask import Flask
    from flask_cors import CORS
    from user_microservices.app_user.dal.user_repository import UserRepository
    from user_microservices.app_user.services.user_service import UserService
    from user_microservices.app_user.controller.user_controller import create_user_blueprint

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    user_repository = UserRepository(db_instance)
    user_service = UserService(user_repository)
    user_blueprint = create_user_blueprint(user_service)
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def run_building_service():
    from flask import Flask
    from flask_cors import CORS
    from building_microservices.app_building.dal.building_repository import BuildingRepository
    from building_microservices.app_building.services.building_service import BuildingService
    from building_microservices.app_building.controllers.building_controller import create_building_blueprint

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    building_repository = BuildingRepository()
    building_service = BuildingService(building_repository)
    building_blueprint = create_building_blueprint(building_service)
    app.register_blueprint(building_blueprint, url_prefix='/api/buildings')
    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)

def run_report_service():
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
    report_repository = ReportRepository(db_instance)
    report_service = ReportService(building_service_client, report_repository)
    report_blueprint = create_report_blueprint(report_service)
    app.register_blueprint(report_blueprint, url_prefix='/api/reports')
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

USER_SERVICE_URL = "http://localhost:5000"
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

        cls.inspector_credentials = {
            "username": USERNAME,
            "password": PASSWORD
        }

        login_url = f"{USER_SERVICE_URL}/api/users/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        for i in range(5):
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                break
            sleep(5)
        assert response.status_code == 200, f"Login failed: {response.json()}"
        cls.token = response.json()['token']
        print(f"Token: {cls.token}")

        cls.building_service_client = BuildingServiceClient(base_url=BUILDING_SERVICE_URL, token=cls.token)
        cls.report_repository = ReportRepository(db_instance)
        cls.report_service = ReportService(cls.building_service_client, cls.report_repository)

    @classmethod
    def tearDownClass(cls):
        cls.user_service_process.terminate()
        cls.user_service_process.join()

        cls.building_service_process.terminate()
        cls.building_service_process.join()

        cls.report_service_process.terminate()
        cls.report_service_process.join()

    def test_fetch_building_details(self):
        address = ADDRESS
        with self.assertRaises(ValueError):
            self.report_service.fetch_building_details(address)

    def test_generate_inspector_report(self):
        inspector_report_data = InspectorReportDTO(
            id=str(ObjectId()),
            customer_report_id=str(ObjectId()),
            fetched_complete_house_details=CompleteHouseDetailsDTO(
                id=str(ObjectId()),
                address="some address",
                year_built="2024",
                total_area=120.0,
                number_of_buildings=1,
                varmeinstallation="varmepumpe",
                ydervaegsmateriale="mursten",
                tagdaekningsmateriale="tegl",
                bygningens_anvendelse="bolig",
                kilde_til_bygningens_materialer="genbrug",
                supplerende_varme="solvarme"
            ),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-06-22",
            inspector_name="Mock Inspector",
            inspector_signature="Mock Signature",
            building_components=[]
        )
        with self.assertRaises(ValueError):
            self.report_service.generate_inspector_report(inspector_report_data)

    def test_create_combined_report(self):
        with self.assertRaises(ValueError):
            self.report_service.create_combined_report(str(ObjectId()), str(ObjectId()))

    def test_get_inspector_report(self):
        report = self.report_service.get_inspector_report(str(ObjectId()))
        self.assertIsNone(report)

    def test_update_inspector_report(self):
        inspector_report_data = InspectorReportDTO(
            id=str(ObjectId()),
            customer_report_id=str(ObjectId()),
            fetched_complete_house_details=CompleteHouseDetailsDTO(
                id=str(ObjectId()),
                address="some address",
                year_built="2024",
                total_area=120.0,
                number_of_buildings=1,
                varmeinstallation="varmepumpe",
                ydervaegsmateriale="mursten",
                tagdaekningsmateriale="tegl",
                bygningens_anvendelse="bolig",
                kilde_til_bygningens_materialer="genbrug",
                supplerende_varme="solvarme"
            ),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-06-22",
            inspector_name="Mock Inspector",
            inspector_signature="Mock Signature",
            building_components=[]
        )
        self.report_service.update_inspector_report(str(ObjectId()), inspector_report_data)

    def test_delete_inspector_report(self):
        self.report_service.delete_inspector_report(str(ObjectId()))

    def test_submit_customer_report(self):
        customer_report_data = CustomerReportDTO(
            id=str(ObjectId()),
            name="Mock Name",
            phone="12345678",
            email="mock@example.com",
            address="mock_address",
            bestilling_oplysninger="some information",
            ejendomsmægler="some realtor",
            ejer_år="2024",
            boet_periode="2 years",
            tilbygninger="none",
            ombygninger="none",
            renoveringer="none",
            andre_bygninger="none",
            tag="tile",
            ydermur="brick",
            indre_vægge="drywall",
            fundamenter="concrete",
            kælder="yes",
            gulve="wood",
            vinduer_døre="double-pane",
            lofter_etageadskillelser="wood",
            vådrum="ceramic",
            vvs="new"
        )
        report_id = self.report_service.submit_customer_report(customer_report_data)
        self.assertIsNotNone(report_id)

    def test_delete_customer_report(self):
        self.report_service.delete_customer_report(str(ObjectId()))

if __name__ == '__main__':
    unittest.main()
