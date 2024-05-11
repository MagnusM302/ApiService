class Invoice:
    def __init__(self, invoice_id, report_id, amount_due, due_date, customer_email):
        self.invoice_id = None
        self.report_id = report_id
        self.amount_due = amount_due
        self.due_date = due_date
        self.customer_email = customer_email

    def __str__(self):
        return f"Invoice ID: {self.invoice_id}, Due: {self.due_date}, Amount: {self.amount_due}, Customer: {self.customer_email}"
