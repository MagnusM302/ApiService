# shared/config.py

import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")

ALLOWED_SERVICE_IDS = {
    'building_microservices',
    'invoice_microservices',
    'report_microservices',
    'user_microservices'
}
