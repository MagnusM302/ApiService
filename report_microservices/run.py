import sys
import os
from multiprocessing import Process
from flask import Flask
from flask_cors import CORS

# Tilføj de nødvendige systemstier for adgang til delte moduler og tjenester
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from report_microservices.app_report.controllers import setup_routes
from report_microservices.app_report.services import ReportService

# Custom module imports from shared
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_report_app():
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing if needed

    # Initialize the report service
    report_service = ReportService()

    # Setup routes with the initialized service
    setup_routes(app, report_service)

    return app

def run_http():
    app = create_report_app()
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=False)

if __name__ == '__main__':
    # Ensure the logging is set up only in the main process
    setup_logging()

    # Start the HTTP server process
    http_process = Process(target=run_http)
    http_process.start()
    http_process.join()
