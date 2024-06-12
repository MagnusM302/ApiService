import os
import sys
from flask import Flask, request
from flask_cors import CORS
import logging

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

set_sys_path()

# Import service-specific modules
from app_report.services.services import ReportService
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from app_report.controllers import create_blueprint  # Ensure correct import
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables
from report_microservices.app_report.data.report_repository import ReportRepository  # Use concrete implementation

# Load environment variables
load_env_variables()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": "*"}})
    
    @app.before_request
    def log_request_info():
        if request.method == 'OPTIONS':
            print(f'OPTIONS request: {request.url}')

    # Create service clients and services
    building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
    report_repository = ReportRepository()
    report_service = ReportService(building_service_client, report_repository)
    print("Initialized service clients and services")
    
    # Register the blueprint with the Flask app
    blueprint = create_blueprint(report_service)
    app.register_blueprint(blueprint, url_prefix='/api/reports')
    print("Blueprint registered")

    app.config['PORT'] = 5006
    return app

def run_http(app):
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_report_http():
    app = create_app()
    run_http(app)

if __name__ == "__main__":
    setup_logging()
    logging.info("Starting Report Service...")
    print("Starting Report Service")
    run_report_http()
