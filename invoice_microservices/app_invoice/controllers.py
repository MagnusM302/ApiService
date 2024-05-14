#invoice_microservices.app_invoice.controllers.py
from flask import request, jsonify, Response
from datetime import datetime
import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import request, jsonify
from shared.json_utils import JsonUtils
from shared.auth_service import JWTService  
from invoice_microservices.app_invoice.services import InvoiceService


def setup_routes(app, invoice_service):
    @app.route('/invoices', methods=['POST'])
    @JWTService.token_required
    @JWTService.role_required(['Inspector'])
    def create_invoice():
        data = request.json
        report_id = data['report_id']
        square_meters = data['square_meters']
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        customer_email = data['customer_email']
        invoice = invoice_service.create_invoice(report_id, square_meters, due_date, customer_email)
        return jsonify(JsonUtils.convert_to_json_serializable(invoice)), 201

    @app.route('/invoices/<invoice_id>', methods=['GET'])
    @JWTService.token_required
    @JWTService.role_required(['Customer', 'Inspector'])
    def get_invoice(invoice_id):
        invoice = invoice_service.get_invoice(invoice_id)
        if invoice:
            return jsonify(JsonUtils.convert_to_json_serializable(invoice)), 200
        else:
            return jsonify({'error': 'Invoice not found'}), 404

    @app.route('/invoices/<invoice_id>', methods=['PUT'])
    @JWTService.token_required
    @JWTService.role_required(['Inspector'])
    def update_payment_status(invoice_id):
        data = request.json
        is_paid = data.get('is_paid', False)
        invoice_service.update_invoice_payment_status(invoice_id, is_paid)
        return Response(status=204)