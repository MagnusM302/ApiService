import os
import sys
def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()

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
