from datetime import datetime
from ..dal.invoice_repository import InvoiceRepository
from ..dto.converters import InvoiceConverter
from ..dto.invoice_dto import InvoiceDTO
from ..client.invoice_service_client import InvoiceServiceClient
from shared.exceptions import ResourceNotFound
from invoice_microservices.app_invoice.services.interface import IInvoiceService
from invoice_microservices.app_invoice.dal.i_invoice_repository import IInvoiceRepository

class InvoiceService(IInvoiceService):
    def __init__(self, repository: InvoiceRepository, building_service_client: InvoiceServiceClient, invoice_converter: InvoiceConverter):
        self.repository = repository
        self.building_service_client = building_service_client
        self.invoice_converter = invoice_converter

    def calculate_price(self, square_meters: float) -> float:
        if square_meters <= 120:
            return 1000
        elif square_meters <= 200:
            return 1500
        elif square_meters <= 300:
            return 2000
        else:
            return 2500

    def create_invoice_dto(self, report_id: str, building_id: str, due_date: datetime, customer_email: str) -> InvoiceDTO:
        # Hent kvadratmeter fra BuildingService
        square_meters_data = self.building_service_client.get_building_square_meters(building_id)
        if not square_meters_data:
            raise ValueError(f"Failed to get square meters for building ID: {building_id}")

        square_meters = square_meters_data.get('samlet_bygningsareal', 0)

        # Beregn beløb
        amount_due = self.calculate_price(square_meters)
        if due_date.date() <= datetime.now().date():
            raise ValueError("Due date must be in the future")
        
        # Opret og gem faktura
        invoice_dto = InvoiceDTO(None, report_id, amount_due, due_date, customer_email)
        invoice = self.invoice_converter.from_dto(invoice_dto)
        saved_invoice = self.repository.save(invoice)
        return self.invoice_converter.to_dto(saved_invoice)

    def get_invoice(self, invoice_id: str) -> InvoiceDTO:
        invoice = self.repository.find(invoice_id)
        if not invoice:
            raise ResourceNotFound("Invoice", invoice_id)
        return self.invoice_converter.to_dto(invoice)

    def update_invoice_payment_status(self, invoice_id: str, is_paid: bool) -> InvoiceDTO:
        invoice = self.repository.find(invoice_id)
        if not invoice:
            raise ResourceNotFound("Invoice", invoice_id)
        
        if invoice.is_paid != is_paid:
            invoice.is_paid = is_paid
            updated_invoice = self.repository.save(invoice)
            return self.invoice_converter.to_dto(updated_invoice)
        return self.invoice_converter.to_dto(invoice)
