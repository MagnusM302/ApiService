import os
import sys
import logging
from flask import Flask, request
from flask_cors import CORS
from multiprocessing import Process
from time import sleep
import requests

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

set_sys_path()

# Load environment variables early
from shared.custom_dotenv import load_env_variables
load_env_variables()

# Import necessary modules
from user_microservices.app_user.controller.user_controller import create_user_blueprint
from user_microservices.app_user.dal.user_repository import UserRepository
from user_microservices.app_user.services.user_service import UserService
from building_microservices.app_building.controllers.building_controller import create_blueprint as create_building_blueprint
from building_microservices.app_building.services.building_service import BuildingService
from building_microservices.app_building.dal.building_repository import BuildingRepository
from invoice_microservices.app_invoice.controllers.invoice_controller import create_invoice_blueprint
from invoice_microservices.app_invoice.dal.invoice_repository import InvoiceRepository
from invoice_microservices.app_invoice.services.invoice_service import InvoiceService
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.services.report_services import ReportService
from shared.database import db_instance
from shared.custom_logging import setup_logging

# Function to create a Flask app and configure CORS
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    @app.before_request
    def log_request_info():
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()
        print(f"Request path: {request.path}")
        print(f"Request headers: {request.headers}")

    def _build_cors_preflight_response():
        response = Flask.response_class()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.status_code = 200
        return response

    return app

# Create individual Flask apps for each service
user_app = create_app()
building_app = create_app()
invoice_app = create_app()
report_app = create_app()

# Register Blueprints with correct URL prefixes
user_repository = UserRepository(db_instance)
user_service = UserService(user_repository)
user_blueprint = create_user_blueprint(user_service)
user_app.register_blueprint(user_blueprint, url_prefix='/api/users')

# Initialize Building Service and create blueprint
building_repository = BuildingRepository()
building_service = BuildingService(building_repository)
building_blueprint = create_building_blueprint(building_service)
building_app.register_blueprint(building_blueprint, url_prefix='/api/buildings')

# Register Invoice Blueprint
invoice_repository = InvoiceRepository(db_instance)
invoice_service = InvoiceService(invoice_repository)
invoice_blueprint = create_invoice_blueprint(invoice_service)
invoice_app.register_blueprint(invoice_blueprint, url_prefix='/api/invoices')

# Register Report Blueprint
building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
report_repository = ReportRepository(db=db_instance)
report_service = ReportService(building_service_client, report_repository)
report_blueprint = create_report_blueprint(report_service)
report_app.register_blueprint(report_blueprint, url_prefix='/api/reports')

# Function to wait until a service is available
def wait_for_service(url, timeout=30):
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            sleep(1)
    return False

# Cached system token to avoid multiple requests
system_token = None

# Function to get the cached system token or request a new one if necessary
def get_system_token(service_id='report_service'):
    global system_token
    if system_token is None:
        print("Sending POST request to generate system token...")
        try:
            response = requests.post(
                'http://localhost:5000/api/users/system-token', 
                json={'service_id': service_id}
            )
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            if response.status_code == 200:
                system_token = response.json()['system_token']
            else:
                raise ValueError("Failed to get system token")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    return system_token

# Functions to run each Flask app
def run_user_http():
    user_app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def run_building_http():
    building_app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)

def run_invoice_http():
    invoice_app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)

def run_report_http():
    report_app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

if __name__ == '__main__':
    setup_logging()
    print("Starting Services...")

    # Start each service in a separate process
    user_process = Process(target=run_user_http)
    building_process = Process(target=run_building_http)
    invoice_process = Process(target=run_invoice_http)
    report_process = Process(target=run_report_http)

    user_process.start()
    building_process.start()
    invoice_process.start()
    report_process.start()

    # Vent på, at User Service er tilgængelig
    user_service_url = 'http://localhost:5000/api/users/health'
    if wait_for_service(user_service_url):
        try:
            # Anmod om systemtoken
            service_id = 'user_service'
            token = get_system_token(service_id)

            # Sæt token i miljøvariablerne
            os.environ['SYSTEM_TOKEN'] = token
            print(f"System token retrieved and set: {token}")
        except Exception as e:
            logging.error(f"Could not retrieve system token: {e}")
            print(f"Could not retrieve system token: {e}")
    else:
        print("User service is not available. Continuing without system token...")

    user_process.join()
    building_process.join()
    invoice_process.join()
    report_process.join()
