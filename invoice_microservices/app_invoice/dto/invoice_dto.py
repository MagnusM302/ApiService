from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class InvoiceDTO(BaseModel):
    invoice_id: Optional[str]
    report_id: str
    amount_due: float
    due_date: datetime
    customer_email: str
    is_paid: bool = False
