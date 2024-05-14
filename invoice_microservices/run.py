import os
import sys
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process

# Set up the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)  # Adding the current directory to the system path
sys.path.append(parent_dir)    # Adding the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure shared utilities and services are accessible
from invoice_microservices.app_invoice.controllers import setup_routes
from invoice_microservices.app_invoice.services import InvoiceService
from shared.custom_logging import setup_logging
from shared.custom_dotenv import load_env_variables

# Load environment variables using the custom function from shared
load_env_variables()

def create_invoice_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Configure CORS as needed.

    # Initialize services
    invoice_service = InvoiceService()

    # Setup routes with the initialized service
    setup_routes(app, invoice_service)

    return app

def run_http():
    app = create_invoice_app()
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)

if __name__ == '__main__':
    # Ensure the logging is set up only in the main process
    setup_logging()

    # Start the HTTP server process
    http_process = Process(target=run_http)
    http_process.start()
    http_process.join()
