# invoice_microservices/app_invoice/dal/i_invoice_respository.py
from abc import ABC, abstractmethod
from invoice_microservices.app_invoice.models.invoice import Invoice

class IInvoiceRepository(ABC):
    @abstractmethod
    def save(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    def find(self, invoice_id: str) -> Invoice:
        pass

    @abstractmethod
    def delete(self, invoice_id: str) -> None:
        pass
