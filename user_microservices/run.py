import os
from flask import Flask
from flask_cors import CORS
from app_user.controllers import setup_routes
from app_user.services import UserService
from shared.auth_service import JWTService
import logging
from logging.handlers import RotatingFileHandler
from multiprocessing import Process

def create_user_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # Initialize services with environment variables
    jwt_secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret_key_here')  # Fallback to a default if not set
    user_service = UserService()
    jwt_service = JWTService(jwt_secret_key)

    # Setup routes with the Flask application instance
    setup_routes(app, user_service, jwt_service)
    
    return app

def run_http():
    app = create_user_app()
    app.run(port=5000)

def run_https():
    app = create_user_app()
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5001)

def run_user_service():
    # Setup processes for HTTP and HTTPS servers
    http_process = Process(target=run_http)
    https_process = Process(target=run_https)

    http_process.start()
    https_process.start()

    http_process.join()  # Optionally wait for the HTTP server process to finish
    https_process.join()  # Optionally wait for the HTTPS server process to finish

if __name__ == '__main__':
    run_user_service()
