import os
import sys
from flask import Flask
from flask_cors import CORS

# Set up the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)  # Adding the current directory to the system path
sys.path.append(parent_dir)    # Adding the parent directory to the system path

# Now we can safely import controller
from building_microservices.app_user.controllers import controller

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(controller)
    return app

def run_http():
    app = create_app()
    # Disable debug mode if running in multiprocessing context
    debug_mode = 'debug' in sys.argv
    app.run(host='0.0.0.0', port=5005, debug=debug_mode)

if __name__ == '__main__':
    run_http()
