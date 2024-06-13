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
from building_microservices.app_building.controllers import create_blueprint
from building_microservices.app_building.services.building_service import BuildingService
from building_microservices.app_building.dal.building_repository import BuildingRepository
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables
load_env_variables()

def create_building_app():
    """Create and configure an instance of the Flask application."""
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
    
    repository = BuildingRepository()
    building_service = BuildingService(repository)
    print("Initialized service clients and services")

    blueprint = create_blueprint(building_service)
    app.register_blueprint(blueprint, url_prefix='/api/buildings')
    print("Blueprint registered")

    app.config['PORT'] = 5005
    return app

def run_http(app):
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_building_http():
    app = create_building_app()
    run_http(app)

if __name__ == "__main__":
    setup_logging()
    logging.info("Starting Building Service...")
    print("Starting Building Service")
    run_building_http()
