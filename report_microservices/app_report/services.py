from dal import ReportRepository
from converters import ReportConverter
from dto import ReportDTO

class ReportService:
    def __init__(self, report_repository):
        self.report_repository = ReportRepository
        self.report_report_dto = ReportDTO
        
    def create_report(self, report_dto):
        # Konverterer fra DTO til Report-domænemodel
        new_report = ReportConverter.from_dto(report_dto)
        # Gemmer Report-domænemodellen i databasen
        saved_report = self.report_repository.save(new_report)
        # Konverterer den gemte Report tilbage til en DTO før den returneres
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
            return ReportConverter.to_dto(updated_report)  # Konverter til DTO før returnering
        else:
            return None

    def get_report(self, report_id):
        report = self.report_repository.find(report_id)
        return ReportConverter.to_dto(report) if report else None  # Konverter til DTO hvis rapporten findes

    def delete_report(self, report_id):
        if self.report_repository.delete(report_id):
            return {"success": True, "message": "Report successfully deleted"}
        else:
            return {"success": False, "message": "Report deletion failed or report not found"}
