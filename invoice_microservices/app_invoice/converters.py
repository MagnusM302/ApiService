#dto_converter.py
from invoice_microservices.app_invoice.dto import InvoiceDTO
from invoice_microservices.app_invoice.models import Invoice

class InvoiceConverter:
    @staticmethod
    def to_dto(invoice):
        """ Konverterer en Invoice instans til en InvoiceDTO. """
        if not invoice:
            return None
        return InvoiceDTO(invoice.invoice_id, invoice.report_id, invoice.amount_due,
                          invoice.due_date, invoice.customer_email)

    @staticmethod
    def from_dto(invoice_dto):
        """ Konverterer en InvoiceDTO tilbage til en Invoice instans. """
        if not invoice_dto:
            return None
        invoice = Invoice(invoice_dto.invoice_id, invoice_dto.report_id, invoice_dto.amount_due,
                          invoice_dto.due_date, invoice_dto.customer_email)
        invoice.invoice_id = invoice_dto.invoice_id  # Sætter ID, hvis det eksisterer
        return invoice
