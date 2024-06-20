from abc import ABC, abstractmethod
from typing import Optional
from ..models.complete_house_details import CompleteHouseDetails
from ..models.customer_report import CustomerReport
from ..models.inspector_report import InspectorReport

class IReportRepository(ABC):
    @abstractmethod
    def get_customer_report_by_id(self, report_id: str) -> Optional[CustomerReport]:
        pass

    @abstractmethod
    def save_customer_report(self, report: CustomerReport):
        pass

    @abstractmethod
    def get_customer_report(self, report_id: str) -> Optional[CustomerReport]:
        pass

    @abstractmethod
    def get_inspector_report(self, report_id: str) -> Optional[InspectorReport]:
        pass

    @abstractmethod
    def update_inspector_report(self, report_id: str, report: InspectorReport) -> None:
        pass

    @abstractmethod
    def delete_inspector_report(self, report_id: str) -> None:
        pass

    @abstractmethod
    def delete_customer_report(self, report_id: str) -> None:
        pass
