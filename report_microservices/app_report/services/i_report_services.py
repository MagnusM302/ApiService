from typing import Protocol
from ..dto.complete_house_details_dto import CompleteHouseDetailsDTO
from ..dto.customer_report_dto import CustomerReportDTO
from ..dto.inspector_report_dto import InspectorReportDTO

class IReportService(Protocol):
    def fetch_building_details(self, address: str) -> CompleteHouseDetailsDTO:
        pass

    def generate_inspector_report(self, customer_report_id: str, building_details: CompleteHouseDetailsDTO) -> InspectorReportDTO:
        pass

    def get_inspector_report(self, report_id: str) -> InspectorReportDTO:
        pass

    def update_inspector_report(self, report_id: str, updated_report: InspectorReportDTO):
        pass

    def delete_inspector_report(self, report_id: str):
        pass

    def submit_customer_report(self, data: CustomerReportDTO) -> str:
        pass

    def create_combined_report(self, customer_report_id: str, inspector_report_id: str) -> InspectorReportDTO:
        pass
    
    def delete_customer_report(self, report_id: str):
        pass
