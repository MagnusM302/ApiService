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

# Import local modules
from user_microservices.app_user.controllers import register_user_routes
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_user_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    register_user_routes(app)
    app.config['PORT'] = 5000
    return app

def run_http(app):
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_user_http():
    app = create_user_app()
    run_http(app)

if __name__ == "__main__":
    setup_logging()
    run_user_http()
