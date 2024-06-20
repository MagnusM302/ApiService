import os
import sys

def set_sys_path():
    """
    Adds current and parent directories to sys.path to allow imports from those directories.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

set_sys_path()

import logging
from flask import Flask, request
from flask_cors import CORS
from shared.custom_dotenv import load_env_variables
from shared.custom_logging import setup_logging
from shared.auth_service import request_system_token
from building_microservices.app_building.controllers.building_controller import create_building_blueprint
from building_microservices.app_building.services.building_service import BuildingService
from building_microservices.app_building.dal.building_repository import BuildingRepository



# Load environment variables from .env file
load_env_variables()

def create_building_app():
    """
    Creates and configures the Flask application for the Building Service.
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type, Authorization"]
        }
    })
    
    @app.before_request
    def log_request_info():
        """
        Logs request information before processing it.
        """
        if request.method == 'OPTIONS':
            return '', 200  # Ensure the preflight request returns 200 OK
    
    # Initialize Building Service
    building_repository = BuildingRepository()
    building_service = BuildingService(building_repository)

    # Register Blueprint with the initialized services
    building_blueprint = create_building_blueprint(building_service)
    app.register_blueprint(building_blueprint, url_prefix='/api/buildings')

    app.config['PORT'] = 5005
    return app

def run_http(app):
    """
    Runs the Flask HTTP server on the specified port.
    """
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_building_http():
    """
    Initializes and runs the Building Service HTTP server.
    """
    app = create_building_app()
    run_http(app)

if __name__ == '__main__':
    # Set up logging configuration
    setup_logging()
    logging.info("Starting Building Service...")
    print("Starting Building Service")

    try:
        # Get system token
        service_id = 'building_service'
        token = request_system_token(service_id)

        # Set the token in the environment
        os.environ['SYSTEM_TOKEN'] = token
    except Exception as e:
        logging.error(f"Could not retrieve system token: {e}")
        print(f"Could not retrieve system token: {e}")

    # Start the Building Service HTTP server
    run_building_http()
