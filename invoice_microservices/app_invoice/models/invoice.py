from datetime import datetime
from uuid import uuid4

class Invoice:
    def __init__(self, report_id, amount_due, due_date, customer_email, is_paid=False, invoice_id=None):
        self.invoice_id = invoice_id or str(uuid4())
        self.report_id = report_id
        self.amount_due = amount_due
        self.due_date = due_date
        self.customer_email = customer_email
        self.is_paid = is_paid
