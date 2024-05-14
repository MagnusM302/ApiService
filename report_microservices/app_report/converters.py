from report_microservices.app_report.models import Report
from report_microservices.app_report.dto import ReportDTO

class ReportConverter:
    @staticmethod
    def to_dto(report):
        """Converts a Report instance to a ReportDTO instance."""
        if not isinstance(report, Report):
            raise ValueError("Provided object is not an instance of Report")
        
        return ReportDTO(
            report_id=report.report_id,
            property_details=report.property_details,
            owner=report.owner,
            status=report.status
        )

    @staticmethod
    def from_dto(report_dto):
        """Converts a ReportDTO instance back into a Report instance."""
        if not isinstance(report_dto, ReportDTO):
            raise ValueError("Provided object is not an instance of ReportDTO")
        
        return Report(
            report_id=report_dto.report_id,
            property_details=report_dto.property_details,
            owner=report_dto.owner,
            status=report_dto.status
        )
