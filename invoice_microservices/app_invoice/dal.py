#invoice_dal.py
from shared.database import Database
from bson.objectid import ObjectId
from models import Invoice

class InvoiceRepository:
    collection = Database.get_collection('invoices')

    @staticmethod
    def save(invoice):
        document = {
            "report_id": ObjectId(invoice.report_id),  # Sikrer, at report_id er korrekt format
            "amount_due": invoice.amount_due,
            "due_date": invoice.due_date,
            "customer_email": invoice.customer_email
        }
        if not invoice.invoice_id:
            result = InvoiceRepository.collection.insert_one(document)
            invoice.invoice_id = str(result.inserted_id)  # Opdaterer invoice objektet med det nye ID
        else:
            InvoiceRepository.collection.update_one(
                {"_id": ObjectId(invoice.invoice_id)},
                {"$set": document}
            )
        return invoice

    @staticmethod
    def find(invoice_id):
        doc = InvoiceRepository.collection.find_one({"_id": ObjectId(invoice_id)})
        if doc:
            # Opretter og returnerer en Invoice instans med data fra databasen
            return Invoice(str(doc['_id']), str(doc['report_id']), doc['amount_due'], doc['due_date'], doc['customer_email'])
        return None

