from ..dto.invoice_dto import InvoiceDTO
from ..models.invoice import Invoice

class InvoiceConverter:
    @staticmethod
    def from_dto(dto: InvoiceDTO) -> Invoice:
        return Invoice(
            invoice_id=dto.invoice_id,
            report_id=dto.report_id,
            amount_due=dto.amount_due,
            due_date=dto.due_date,
            customer_email=dto.customer_email,
            is_paid=dto.is_paid
        )

    @staticmethod
    def to_dto(invoice: Invoice) -> InvoiceDTO:
        return InvoiceDTO(
            invoice_id=invoice.invoice_id,
            report_id=invoice.report_id,
            amount_due=invoice.amount_due,
            due_date=invoice.due_date,
            customer_email=invoice.customer_email,
            is_paid=invoice.is_paid
        )
