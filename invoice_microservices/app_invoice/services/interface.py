from abc import ABC, abstractmethod
from datetime import datetime
from invoice_microservices.app_invoice.dto.invoice_dto import InvoiceDTO

class IInvoiceService(ABC):
    @abstractmethod
    def calculate_price(self, square_meters: float) -> float:
        pass

    @abstractmethod
    def create_invoice_dto(self, report_id: str, square_meters: float, due_date: datetime, customer_email: str) -> InvoiceDTO:
        pass

    @abstractmethod
    def get_invoice(self, invoice_id: str) -> InvoiceDTO:
        pass

    @abstractmethod
    def update_invoice_payment_status(self, invoice_id: str, is_paid: bool) -> InvoiceDTO:
        pass
