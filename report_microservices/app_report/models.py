class Report:
    def __init__(self, report_id, property_details, owner, status='pending'):
        self.report_id = report_id
        self.property_details = property_details
        self.owner = owner
        self.status = status  # default status er 'pending'

    def __str__(self):
        return (f"Report ID: {self.report_id}, Property: {self.property_details}, "
                f"Owner: {self.owner}, Status: {self.status}")
