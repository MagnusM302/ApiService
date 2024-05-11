class InvoiceDTO:
    def __init__(self, invoice_id, report_id, amount_due, due_date, customer_email):
        self.invoice_id = invoice_id
        self.report_id = report_id
        self.amount_due = amount_due
        self.due_date = due_date
        self.customer_email = customer_email

    def __repr__(self):
        return (f"InvoiceDTO(ID: {self.invoice_id}, Due: {self.due_date}, "
                f"Amount: {self.amount_due}, Customer: {self.customer_email})")
