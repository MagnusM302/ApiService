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

# Ensure shared utilities and services are accessible
from invoice_microservices.app_invoice.controllers.invoice_controller import invoice_blueprint
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_invoice_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Setup routes with the initialized services
    app.register_blueprint(invoice_blueprint, url_prefix='/api/invoices')
    return app

def run_http(app):
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)

def run_invoice_http():
    app = create_invoice_app()
    run_http(app)

if __name__ == '__main__':
    # Ensure the logging is set up only in the main process
    setup_logging()
    run_invoice_http()
