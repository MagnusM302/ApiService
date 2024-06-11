from flask import Blueprint, request, jsonify
from shared.auth_service import JWTService
from invoice_microservices.app_invoice.services.invoice_service import InvoiceService
from invoice_microservices.app_invoice.services.interface import IInvoiceService
from datetime import datetime
from shared.exceptions import ResourceNotFound

invoice_service: IInvoiceService = InvoiceService()

invoice_blueprint = Blueprint('invoice', __name__)

@invoice_blueprint.route('/create_invoice', methods=['POST'])
@JWTService.token_required
@JWTService.role_required(['INSPECTOR'])
def create_invoice():
    data = request.json
    try:
        report_id = data['report_id']
        square_meters = data['square_meters']
        due_date = datetime.fromisoformat(data['due_date'])
        customer_email = data['customer_email']

        invoice_dto = invoice_service.create_invoice_dto(report_id, square_meters, due_date, customer_email)
        return jsonify(invoice_dto.one_dump()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoice_blueprint.route('/invoice/<invoice_id>', methods=['GET'])
@JWTService.token_required
@JWTService.role_required(['INSPECTOR'])
def get_invoice(invoice_id):
    try:
        invoice_dto = invoice_service.get_invoice(invoice_id)
        return jsonify(invoice_dto.one_dump()), 200
    except ResourceNotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoice_blueprint.route('/invoice/<invoice_id>/payment_status', methods=['PUT'])
@JWTService.token_required
@JWTService.role_required(['INSPECTOR'])
def update_invoice_payment_status(invoice_id):
    data = request.json
    try:
        is_paid = data['is_paid']
        invoice_dto = invoice_service.update_invoice_payment_status(invoice_id, is_paid)
        return jsonify(invoice_dto.one_dump()), 200
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except ResourceNotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
