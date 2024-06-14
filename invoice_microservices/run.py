import os
import sys

def set_sys_path():
    """
    Adds current and parent directories to sys.path to allow imports from those directories.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
    parent_dir = os.path.dirname(current_dir)  # Get the parent directory of the current directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Get the root directory
    sys.path.append(current_dir)  # Add the current directory to sys.path
    sys.path.append(parent_dir)  # Add the parent directory to sys.path
    sys.path.append(root_dir)  # Add the root directory to sys.path

# Ensure sys.path is correctly set up before importing other modules
set_sys_path()

# Import necessary modules
import logging  # For logging messages
from flask import Flask, request  # Flask for creating the web application
from flask_cors import CORS  # Flask-CORS for handling Cross-Origin Resource Sharing (CORS)
from shared.custom_dotenv import load_env_variables  # Function to load environment variables
from shared.custom_logging import setup_logging  # Function to set up logging configuration
from shared.auth_service import request_system_token  # Function to request system token
from invoice_microservices.app_invoice.controllers.invoice_controller import create_invoice_blueprint  # Function to create the invoice blueprint
from invoice_microservices.app_invoice.dal.invoice_repository import InvoiceRepository  # Invoice repository class
from invoice_microservices.app_invoice.services.invoice_service import InvoiceService  # Invoice service class
from shared.database import db_instance  # Database instance

# Load environment variables using the custom function from shared
load_env_variables()

def create_invoice_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",  # Allow all origins
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow these methods
            "allow_headers": ["Content-Type", "Authorization"]  # Allow these headers
        }
    })
    
    @app.before_request
    def log_request_info():
        if request.method == 'OPTIONS':
            print(f'OPTIONS request: {request.url}')  # Log OPTIONS requests
    
    # Initialize the database
    db_instance.initialize()  # Ensure the database is initialized if necessary

    # Setup InvoiceService
    invoice_repository = InvoiceRepository(db_instance)  # Create an instance of InvoiceRepository
    invoice_service = InvoiceService(invoice_repository)  # Create an instance of InvoiceService

    # Setup routes with the initialized services
    invoice_blueprint = create_invoice_blueprint(invoice_service)  # Create the invoice blueprint
    app.register_blueprint(invoice_blueprint, url_prefix='/api/invoices')  # Register the blueprint with the app
    print("Blueprint registered")
    
    app.config['PORT'] = 5002  # Set the port for the app
    return app

def run_http(app):
    """Run the HTTP server."""
    print(f"Running HTTP server on port {app.config['PORT']}")
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True, use_reloader=False)  # Start the Flask app

def run_invoice_http():
    """Create and run the Invoice HTTP server."""
    app = create_invoice_app()  # Create the invoice app
    run_http(app)  # Run the HTTP server

if __name__ == '__main__':
    setup_logging()  # Set up logging configuration
    logging.info("Starting Invoice Service...")  # Log the start of the service
    print("Starting Invoice Service")

    try:
        # Get system token
        service_id = 'invoice_service'
        token = request_system_token(service_id)  # Request a system token for the service

        # Set the token in the environment
        os.environ['SYSTEM_TOKEN'] = token  # Store the token in the environment variables
    except Exception as e:
        logging.error(f"Could not retrieve system token: {e}")  # Log an error if the token could not be retrieved
        print(f"Could not retrieve system token: {e}")  # Print the error

    run_invoice_http()  # Run the invoice HTTP server
