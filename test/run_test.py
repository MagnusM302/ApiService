# test/integration_test.py
import sys
import os
import unittest

def add_project_to_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

add_project_to_sys_path()

import requests
from multiprocessing import Process
from time import sleep
from report_microservices.app_report.services.report_services import ReportService
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from report_microservices.app_report.dal.i_report_repository import IReportRepository
from report_microservices.app_report.controllers import create_report_blueprint
from flask import Flask

class MockReportRepository(IReportRepository):
    def __init__(self):
        self.reports = []

    def save_report(self, report_dto):
        self.reports.append(report_dto)

def run_user_service():
    from user_microservices.app_user.controller.user_controller import create_user_blueprint
    from user_microservices.app_user.dal.user_repository import UserRepository
    from user_microservices.app_user.services.user_service import UserService
    from shared.database import db_instance
    from flask_cors import CORS
    from shared.custom_dotenv import load_env_variables

    load_env_variables()

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
    from building_microservices.app_building.controllers.building_controller import create_blueprint as create_building_blueprint
    from building_microservices.app_building.dal.building_repository import BuildingRepository
    from building_microservices.app_building.services.building_service import BuildingService
    from flask_cors import CORS
    from flask import Flask

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
    from shared.custom_dotenv import load_env_variables
    from shared.database import db_instance

    load_env_variables()

    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
    report_repository = MockReportRepository()
    report_service = ReportService(building_service_client, report_repository)
    report_blueprint = create_report_blueprint(report_service)
    app.register_blueprint(report_blueprint, url_prefix='/api/reports')
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

USERNAME = "tryk12"
PASSWORD = "12345678"
ADDRESS = "kærvej 7, 9800"

class TestBuildingService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_service_process = Process(target=run_user_service)
        cls.building_service_process = Process(target=run_building_service)
        cls.report_service_process = Process(target=run_report_service)
        
        cls.user_service_process.start()
        cls.building_service_process.start()
        cls.report_service_process.start()
        
        sleep(40)  # Give the services time to start

        login_url = "http://localhost:5000/api/users/login"
        login_data = {"username": USERNAME, "password": PASSWORD}
        for _ in range(5):
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                break
            sleep(5)
        assert response.status_code == 200, f"Login failed: {response.json()}"
        cls.token = response.json()['token']
        print(f"Token: {cls.token}")

    @classmethod
    def tearDownClass(cls):
        cls.user_service_process.terminate()
        cls.user_service_process.join()
        
        cls.building_service_process.terminate()
        cls.building_service_process.join()

        cls.report_service_process.terminate()
        cls.report_service_process.join()

    def test_generate_report(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post("http://localhost:5006/api/reports/generate_report", json={'address': ADDRESS}, headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to generate report: {response.json()}")
        report_data = response.json()
        self.assertEqual(report_data['address'], ADDRESS)

    def test_get_generated_report(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post("http://localhost:5006/api/reports/generate_report", json={'address': ADDRESS}, headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to generate report: {response.json()}")
        report_id = response.json()['id']

        response = requests.get(f"http://localhost:5006/api/reports/get_report/{report_id}", headers=headers)
        self.assertEqual(response.status_code, 200, f"Failed to get report: {response.json()}")
        report_data = response.json()
        self.assertEqual(report_data['id'], report_id)
        self.assertEqual(report_data['address'], ADDRESS)

if __name__ == '__main__':
    unittest.main()

