import os
import sys

# Tilføj projektets rodmappe til sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

# Debug print for at sikre, at stien er korrekt
print("Current Directory:", current_dir)
print("Project Root:", project_root)
print("sys.path:", sys.path)
import logging
from flask import Flask
from flask_cors import CORS
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from report_microservices.app_report.services.report_services import ReportService
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from shared.database import db_instance
from shared.auth_service import request_system_token  # Importér funktion til at anmode om systemtoken
from shared.custom_dotenv import load_env_variables  # Importér funktion til at indlæse miljøvariabler
from shared.custom_logging import setup_logging  # Importér funktion til at opsætte logning

# Indlæs miljøvariabler
load_env_variables()

def create_app():
    """
    Opret og konfigurer en instans af Flask-applikationen.
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    return app

# Opret Flask-app til report service
report_app = create_app()

# Initialize Building Service Client og Report Service
building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
report_repository = ReportRepository(db=db_instance)
report_service = ReportService(building_service_client, report_repository)
report_blueprint = create_report_blueprint(report_service)
report_app.register_blueprint(report_blueprint, url_prefix='/api')

def run_report_http():
    """
    Kør HTTP-serveren til report service.
    """
    report_app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

if __name__ == '__main__':
    # Opsæt logning
    setup_logging()
    logging.info("Starting Report Service...")
    print("Starting Report Service")

    try:
        # Anmod om systemtoken
        service_id = 'report_service'
        token = request_system_token(service_id)
        
        # Sæt token i miljøvariablerne
        os.environ['SYSTEM_TOKEN'] = token
    except Exception as e:
        logging.error(f"Could not retrieve system token: {e}")
        print(f"Could not retrieve system token: {e}")

    # Kør report HTTP-server
    run_report_http()
