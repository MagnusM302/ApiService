import sys
import os
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process
from app_invoice.controllers import setup_routes

# Ensure shared utilities and services are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)  # Assuming related logic is in the same directory
sys.path.append(parent_dir)

from app_invoice.services import InvoiceService
from app_invoice.dal import InvoiceRepository
from app_invoice.converters import InvoiceConverter

def create_invoice_app():
    app = Flask(__name__)
    CORS(app)

    # Correctly create instances of dependencies
    invoice_repository = InvoiceRepository()
    invoice_converter = InvoiceConverter()

    # Correct initialization of InvoiceService
    invoice_service = InvoiceService(invoice_repository, invoice_converter)

    # Define all your Flask routes
    setup_routes(app, invoice_service)
    
    return app

def run_http():
    app = create_invoice_app()
    app.run(port=5004)

def run_https():
    app = create_invoice_app()
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5005)

def run_servers():
    # Setup HTTP and HTTPS servers using multiprocessing
    http_process = Process(target=run_http)
    https_process = Process(target=run_https)
    
    http_process.start()
    https_process.start()

    http_process.join()  # Optionally wait for the HTTP server process to finish
    https_process.join()  # Optionally wait for the HTTPS server process to finish

if __name__ == '__main__':
    run_servers()
