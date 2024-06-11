import os
import sys
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process

def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

set_sys_path()

# Import service-specific modules
from building_microservices.app_building.controllers import create_blueprint
from building_microservices.app_building.services.service import BuildingService
from building_microservices.app_building.datalag.dal import BuildingRepository
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables
load_env_variables()

def create_building_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    repository = BuildingRepository()
    building_service = BuildingService(repository)
    blueprint = create_blueprint(building_service)
    app.register_blueprint(blueprint, url_prefix='/api/buildings')
    app.config['PORT'] = 5005
    return app

def run_http(app):
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_building_http():
    app = create_building_app()
    run_http(app)

if __name__ == "__main__":
    setup_logging()
    run_building_http()
