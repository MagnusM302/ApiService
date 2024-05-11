import os
import sys
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process

# Setup to include the project directory to sys.path for easier module imports
api_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if api_service_path not in sys.path:
    sys.path.append(api_service_path)

# Import local modules
from app_user.controllers import setup_routes
from app_user.services import UserService
from shared.auth_service import JWTService

# Custom module imports from shared
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

# Setup logging using the custom function from shared
setup_logging()

def create_user_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize services with environment variables
    jwt_secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key_here')
    user_service = UserService()
    jwt_service = JWTService(jwt_secret_key)

    # Setup routes with the Flask application instance
    setup_routes(app, user_service, jwt_service)
    
    return app

def run_http():
    app = create_user_app()
    app.run(port=5000, debug=True, use_reloader=False)


def run_user_service():
    """Run HTTP version of the app in a separate process."""
    http_process = Process(target=run_http)
    http_process.start()
    http_process.join()

if __name__ == '__main__':
    run_user_service()
