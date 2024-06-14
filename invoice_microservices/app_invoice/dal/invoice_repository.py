from shared.database import Database
from bson.objectid import ObjectId
from invoice_microservices.app_invoice.models.invoice import Invoice
from invoice_microservices.app_invoice.dal.i_invoice_repository import IInvoiceRepository

class InvoiceRepository(IInvoiceRepository):
    def __init__(self, db: Database):
        self.collection = db.get_collection('invoices')

    @staticmethod
    def save(invoice: Invoice) -> Invoice:
        document = {
            "report_id": ObjectId(invoice.report_id),
            "amount_due": invoice.amount_due,
            "due_date": invoice.due_date,
            "customer_email": invoice.customer_email,
            "is_paid": invoice.is_paid
        }
        if not invoice.invoice_id:
            result = InvoiceRepository.collection.insert_one(document)
            invoice.invoice_id = str(result.inserted_id)
        else:
            InvoiceRepository.collection.update_one(
                {"_id": ObjectId(invoice.invoice_id)},
                {"$set": document}
            )
        return invoice

    @staticmethod
    def find(invoice_id: str) -> Invoice:
        doc = InvoiceRepository.collection.find_one({"_id": ObjectId(invoice_id)})
        if doc:
            return Invoice(
                invoice_id=str(doc['_id']),
                report_id=str(doc['report_id']),
                amount_due=doc['amount_due'],
                due_date=doc['due_date'],
                customer_email=doc['customer_email'],
                is_paid=doc['is_paid']
            )
        return None

    @staticmethod
    def delete(invoice_id: str) -> None:
        InvoiceRepository.collection.delete_one({"_id": ObjectId(invoice_id)})
