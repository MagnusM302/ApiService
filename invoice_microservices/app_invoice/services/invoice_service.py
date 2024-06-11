from datetime import datetime
from ..data.invoice_respository import InvoiceRepository
from ..dto.converters import InvoiceConverter
from ..dto.invoice_dto import InvoiceDTO
from shared.exceptions import ResourceNotFound
from invoice_microservices.app_invoice.services.interface import IInvoiceService
from invoice_microservices.app_invoice.data.interface import IInvoiceRepository


class InvoiceService(IInvoiceService):
    def __init__(self, repository: IInvoiceRepository = InvoiceRepository()):
        self.invoice_repository = repository
        self.invoice_converter = InvoiceConverter()

    def calculate_price(self, square_meters: float) -> float:
        if square_meters <= 120:
            return 1000
        elif square_meters <= 200:
            return 1500
        elif square_meters <= 300:
            return 2000
        else:
            return 2500

    def create_invoice_dto(self, report_id: str, square_meters: float, due_date: datetime, customer_email: str) -> InvoiceDTO:
        amount_due = self.calculate_price(square_meters)
        if due_date.date() <= datetime.now().date():
            raise ValueError("Due date must be in the future")
        
        invoice_dto = InvoiceDTO(None, report_id, amount_due, due_date, customer_email)
        invoice = self.invoice_converter.from_dto(invoice_dto)
        saved_invoice = self.invoice_repository.save(invoice)
        return self.invoice_converter.to_dto(saved_invoice)

    def get_invoice(self, invoice_id: str) -> InvoiceDTO:
        invoice = self.invoice_repository.find(invoice_id)
        if not invoice:
            raise ResourceNotFound("Invoice", invoice_id)
        return self.invoice_converter.to_dto(invoice)

    def update_invoice_payment_status(self, invoice_id: str, is_paid: bool) -> InvoiceDTO:
        invoice = self.invoice_repository.find(invoice_id)
        if not invoice:
            raise ResourceNotFound("Invoice", invoice_id)
        
        if invoice.is_paid != is_paid:
            invoice.is_paid = is_paid
            updated_invoice = self.invoice_repository.save(invoice)
            return self.invoice_converter.to_dto(updated_invoice)
        return self.invoice_converter.to_dto(invoice)