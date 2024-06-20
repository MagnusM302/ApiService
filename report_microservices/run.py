import os
import sys

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()

import logging
from flask import Flask
from flask_cors import CORS
from shared.custom_dotenv import load_env_variables
from shared.custom_logging import setup_logging
from shared.auth_service import request_system_token
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from report_microservices.app_report.services.report_services import ReportService
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from shared.database import db_instance



load_env_variables()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    return app

report_app = create_app()

building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
report_repository = ReportRepository(db=db_instance)
report_service = ReportService(building_service_client, report_repository)
report_blueprint = create_report_blueprint(report_service)
report_app.register_blueprint(report_blueprint, url_prefix='/api/reports')

def run_report_http():
    report_app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

if __name__ == '__main__':
    setup_logging()
    logging.info("Starting Report Service...")
    try:
        service_id = 'report_service'
        token = request_system_token(service_id)
        os.environ['SYSTEM_TOKEN'] = token
    except Exception as e:
        logging.error(f"Could not retrieve system token: {e}")
    run_report_http()
