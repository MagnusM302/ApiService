from typing import Protocol
from ..dto.complete_house_details_dto import CompleteHouseDetailsDTO
from ..dto.customer_report_dto import CustomerReportDTO

class IReportService(Protocol):
    def generate_report(self, building_id: str, address_id: str, manual_data: dict = None) -> CompleteHouseDetailsDTO:
        pass

    def get_report(self, report_id: str) -> CompleteHouseDetailsDTO:
        pass

    def update_report(self, report_id: str, updated_report: CompleteHouseDetailsDTO):
        pass

    def delete_report(self, report_id: str):
        pass

    def submit_customer_report(self, data: dict) -> str:
        pass

    def create_complete_report(self, customer_report_id: str) -> CompleteHouseDetailsDTO:
        pass
    
    def delete_customer_report(self, report_id: str):
        pass

    def create_complete_report(self, customer_report_id: str) -> CompleteHouseDetailsDTO:
        pass
