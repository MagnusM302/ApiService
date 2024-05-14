from report_microservices.app_report.dal import ReportRepository
from report_microservices.app_report.converters import ReportConverter
from report_microservices.app_report.dto import ReportDTO

class ReportService:
    def __init__(self):
        self.report_repository = ReportRepository  # Pass an instance, not the class
        
    def create_report(self, report_dto):
        new_report = ReportConverter.from_dto(report_dto)
        saved_report = self.report_repository.save(new_report)
        return ReportConverter.to_dto(saved_report)

    def update_report(self, report_id, property_details=None, owner=None, status=None):
        report = self.report_repository.find(report_id)
        if report:
            if property_details:
                report.property_details = property_details
            if owner:
                report.owner = owner
            if status:
                report.status = status
            updated_report = self.report_repository.save(report)
            return ReportConverter.to_dto(updated_report)
        else:
            return None

    def get_report(self, report_id):
        report = self.report_repository.find(report_id)
        return ReportConverter.to_dto(report) if report else None

    def delete_report(self, report_id):
        return {"success": self.report_repository.delete(report_id), "message": "Report successfully deleted" if self.report_repository.delete(report_id) else "Report deletion failed or report not found"}
