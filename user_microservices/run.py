import os
import sys
import time
import requests
from flask import Flask, request
from flask_cors import CORS
import logging

def set_sys_path():
    """
    Tilføjer nuværende og overordnede mapper til sys.path for at tillade imports fra disse mapper.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

set_sys_path()

# Import service-specifikke moduler
from user_microservices.app_user.controller.user_controller import create_user_blueprint
from user_microservices.app_user.dal.user_repository import UserRepository
from user_microservices.app_user.services.user_service import UserService
from shared.database import Database
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables
from shared.auth_service import request_system_token

# Indlæs miljøvariabler ved hjælp af den tilpassede funktion fra shared
load_env_variables()

def wait_for_service(url, timeout=30):
    """
    Vent på, at tjenesten bliver tilgængelig inden for timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(1)
    return False

def create_user_app():
    """Opret og konfigurer en instans af Flask-applikationen."""
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
        if request.method == 'OPTIONS':
            print(f'OPTIONS request: {request.url}')
            return '', 200  # Sikrer at preflight request returnerer 200 OK
    
    # Initialiser databasen
    Database.initialize()

    # Opsæt UserService
    user_repository = UserRepository(Database.db)
    user_service = UserService(user_repository)

    # Opsæt ruter med de initialiserede services
    user_blueprint = create_user_blueprint(user_service)
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    print("Blueprint registered")
    
    app.config['PORT'] = 5000
    return app

def run_http(app):
    """
    Kør HTTP-serveren på den specificerede port.
    """
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_user_http():
    """
    Initialiser og kør Flask-app for user service.
    """
    app = create_user_app()
    run_http(app)

if __name__ == '__main__':
    setup_logging()
    logging.info("Starting User Service...")
    print("Starting User Service")

    run_user_http()

    # Vent på, at User Service er tilgængelig
    user_service_url = 'http://localhost:5000/api/users/health'

    if wait_for_service(user_service_url):
        try:
            # Anmod om systemtoken
            service_id = 'user_service'
            token = request_system_token(service_id)

            # Sæt token i miljøvariablerne
            os.environ['SYSTEM_TOKEN'] = token
            print(f"System token retrieved and set: {token}")
        except Exception as e:
            logging.error(f"Could not retrieve system token: {e}")
            print(f"Could not retrieve system token: {e}")
    else:
        print("User service is not available. Continuing without system token...")
