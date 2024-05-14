import os
import sys
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process

# Set up the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)  # Assuming related logic is in the same directory
sys.path.append(parent_dir)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import local modules
from app_user.controllers import setup_routes
from user_microservices.app_user.services import UserService

# Custom module imports from shared
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_user_app():
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing if needed
    user_service = UserService()
    setup_routes(app, user_service)
    return app

def run_http():
    app = create_user_app()
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    # Ensure the logging is set up only in the main process
    setup_logging()

    # Start the HTTP server process
    http_process = Process(target=run_http)
    http_process.start()
    http_process.join()
