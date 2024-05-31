#!/bin/bash

echo "Starting all services..."

# Start User Service
gunicorn -w 4 -b 0.0.0.0:5000 user_microservices.run:create_user_app --daemon

# Start Report Service
gunicorn -w 4 -b 0.0.0.0:5001 report_microservices.run:create_report_app --daemon

# Start Invoice Service
gunicorn -w 4 -b 0.0.0.0:5002 invoice_microservices.run:create_invoice_app --daemon

# Start Building Service
gunicorn -w 4 -b 0.0.0.0:5003 building_microservices.run:create_building_app --daemon

echo "All services are started."
