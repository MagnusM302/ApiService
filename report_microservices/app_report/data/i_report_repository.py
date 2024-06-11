from typing import Protocol, Optional
from ..models.complete_house_details import CompleteHouseDetails
from ..models.customer_report import CustomerReport

class IReportRepository(Protocol):
    def save_report(self, report: CompleteHouseDetails):
        pass

    def get_report(self, report_id: str) -> Optional[CompleteHouseDetails]:
        pass

    def update_report(self, report_id: str, report: CompleteHouseDetails):
        pass

    def delete_report(self, report_id: str):
        pass
    
    def save_customer_report(self, report: CustomerReport):
        pass

    def get_customer_report(self, report_id: str) -> Optional[CustomerReport]:
        pass
    
    def delete_customer_report(self, report_id: str):
        pass
