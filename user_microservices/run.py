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
from user_microservices.app_user.controller.user_controller import create_user_blueprint
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_user_app():
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
            return '', 200  # Ensure the preflight request returns 200 OK
    
    # Setup routes with the initialized services
    user_blueprint = create_user_blueprint()
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    print("Blueprint registered")
    
    app.config['PORT'] = 5000
    return app

def run_http(app):
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)

def run_user_http():
    app = create_user_app()
    run_http(app)

if __name__ == '__main__':
    setup_logging()
    logging.info("Starting User Service...")
    print("Starting User Service")
    run_user_http()
