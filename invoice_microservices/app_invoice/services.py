from datetime import datetime
from converters import InvoiceConverter
from dto import InvoiceDTO
from dal import InvoiceRepository
from shared.exceptions import ResourceNotFound

class InvoiceService:
    def __init__(self, invoice_repository, invoice_converter):
        self.invoice_repository = invoice_repository
        self.invoice_converter = invoice_converter

    def calculate_price(self, square_meters):
        """Calculate the price based on the property's square meters."""
        if square_meters <= 120:
            return 1000
        elif square_meters <= 200:
            return 1500
        elif square_meters <= 300:
            return 2000
        else:
            return 2500

    def create_invoiceDto(self, report_id, square_meters, due_date, customer_email):
        """Create and save a new invoice from a DTO."""
        amount_due = self.calculate_price(square_meters)
        if due_date.date() <= datetime.now().date():
            raise ValueError("Due date must be in the future")
        
        # Create DTO
        invoice_dto = InvoiceDTO(None, report_id, amount_due, due_date, customer_email)
        
        # Convert DTO to model
        invoice = self.invoice_converter.from_dto(invoice_dto)
        
        # Save model to the database
        saved_invoice = self.invoice_repository.save(invoice)
        
        # Optionally, return the updated DTO, or convert saved model back to DTO
        return self.invoice_converter.to_dto(saved_invoice)

    def get_invoice(self, invoice_id):
        """Retrieve an invoice by its ID."""
        invoice = self.invoice_repository.find(invoice_id)
        if not invoice:
            raise ResourceNotFound("Invoice", invoice_id)
        return self.invoice_converter.to_dto(invoice)

    def update_invoice_payment_status(self, invoice_id, is_paid):
        """Update the payment status of an invoice."""
        invoice = self.invoice_repository.find(invoice_id)
        if not invoice:
           raise ResourceNotFound("Invoice", invoice_id)
        
        if invoice.is_paid != is_paid:
            invoice.is_paid = is_paid
            updated_invoice = self.invoice_repository.save(invoice)
            return self.invoice_converter.to_dto(updated_invoice)
        return self.invoice_converter.to_dto(invoice)
