from flask import Flask
from flask_cors import CORS
from report_microservices.app_report.controllers.report_controller import create_report_blueprint
from report_microservices.app_report.services.report_services import ReportService
from report_microservices.app_report.dal.report_repository import ReportRepository
from report_microservices.app_report.client.building_service_client import BuildingServiceClient

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

# Initialize Building Service Client and Report Service
building_service_client = BuildingServiceClient(base_url="http://localhost:5005/api")
report_repository = ReportRepository()
report_service = ReportService(building_service_client, report_repository)
report_blueprint = create_report_blueprint(report_service)
report_app.register_blueprint(report_blueprint, url_prefix='/api')

def run_report_http():
    report_app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_report_http()
