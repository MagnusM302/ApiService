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

from app_report.services import ReportService
from app_report.dal import ReportRepository
from app_report.controllers import setup_routes

def create_report_app():
    app = Flask(__name__)
    CORS(app)  # Aktivér CORS for alle ruter

    # Opret tjeneste med dens afhængigheder
    report_service = ReportService(ReportRepository())

    # Definer ruter via controller
    setup_routes(app, report_service)

    return app

def run_http():
    app = create_report_app()
    app.run(port=5002)

def run_https():
    app = create_report_app()
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5003)

def run_servers():
    # Opsætning af HTTP og HTTPS servere ved hjælp af multiprocessing
    http_process = Process(target=run_http)
    https_process = Process(target=run_https)
    
    http_process.start()
    https_process.start()

    http_process.join()  # Vent eventuelt på, at HTTP-serverprocessen afsluttes
    https_process.join()  # Vent eventuelt på, at HTTPS-serverprocessen afsluttes

if __name__ == '__main__':
    run_servers()
