from typing import Optional
from bson.objectid import ObjectId
from ..models.complete_house_details import CompleteHouseDetails
from ..models.customer_report import CustomerReport
from ..models.inspector_report import InspectorReport
from .i_report_repository import IReportRepository
from enum import Enum
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from shared.database import Database
import logging

class ReportRepository(IReportRepository):
    def __init__(self, db: Database):
        self.inspector_report_collection = db.get_collection('inspector_reports')
        self.customer_report_collection = db.get_collection('customer_reports')
    
    def save_inspector_report(self, report: InspectorReport) -> InspectorReport:
        report_dict = report.model_dump()  # Use `model_dump()` method of Pydantic model
        report_dict = self.convert_enums(report_dict)
        result = self.inspector_report_collection.insert_one(report_dict)
        report.id = str(result.inserted_id)  # Update the report object with the generated ID
        logging.info(f"Saved inspector report with ID: {report.id}")
        return report

    def get_inspector_report(self, report_id: str) -> Optional[InspectorReport]:
        report_data = self.inspector_report_collection.find_one({"_id": ObjectId(report_id)})
        if report_data:
            report_data = self.reconstruct_enums(report_data)
            logging.info(f"Retrieved inspector report with ID: {report_id}")
            return InspectorReport(**report_data)
        logging.warning(f"Inspector report with ID: {report_id} not found")
        return None

    def update_inspector_report(self, report_id: str, report: InspectorReport) -> None:
        report_dict = report.model_dump()
        report_dict = self.convert_enums(report_dict)
        self.inspector_report_collection.update_one({"_id": ObjectId(report_id)}, {"$set": report_dict})
        logging.info(f"Updated inspector report with ID: {report_id}")

    def delete_inspector_report(self, report_id: str) -> None:
        self.inspector_report_collection.delete_one({"_id": ObjectId(report_id)})
        logging.info(f"Deleted inspector report with ID: {report_id}")
    
    def save_customer_report(self, customer_report: CustomerReport) -> CustomerReport:
        customer_report_dict = customer_report.model_dump()
        result = self.customer_report_collection.insert_one(customer_report_dict)
        customer_report.id = str(result.inserted_id)  # Update the customer report object with the generated ID
        logging.info(f"Saved customer report with ID: {customer_report.id}")
        return customer_report

    def get_customer_report(self, report_id: str) -> Optional[CustomerReport]:
        customer_report_data = self.customer_report_collection.find_one({"_id": ObjectId(report_id)})
        if customer_report_data:
            customer_report_data = self.reconstruct_enums(customer_report_data)
            logging.info(f"Retrieved customer report with ID: {report_id}")
            return CustomerReport(**customer_report_data)
        logging.warning(f"Customer report with ID: {report_id} not found")
        return None
    
    def update_customer_report(self, report_id: str, customer_report: CustomerReport) -> None:
        customer_report_dict = customer_report.model_dump()
        customer_report_dict = self.convert_enums(customer_report_dict)
        self.customer_report_collection.update_one({"_id": ObjectId(report_id)}, {"$set": customer_report_dict})
        logging.info(f"Updated customer report with ID: {report_id}")

    def delete_customer_report(self, report_id: str) -> None:
        self.customer_report_collection.delete_one({"_id": ObjectId(report_id)})
        logging.info(f"Deleted customer report with ID: {report_id}")
        
    def get_customer_report_by_id(self, report_id: str) -> Optional[CustomerReport]:
        logging.info(f"Fetching customer report with ID: {report_id}")
        customer_report_data = self.customer_report_collection.find_one({"_id": ObjectId(report_id)})
        if customer_report_data:
            customer_report_data = self.reconstruct_enums(customer_report_data)
            logging.info(f"Retrieved customer report with ID: {report_id}")
            return CustomerReport(**customer_report_data)
        logging.warning(f"Customer report with ID: {report_id} not found")
        return None

    def convert_enums(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, Enum):
                    d[k] = v.value
                elif isinstance(v, list):
                    d[k] = [self.convert_enums(item) for item in v]
                elif isinstance(v, dict):
                    d[k] = self.convert_enums(v)
        elif isinstance(d, list):
            d = [self.convert_enums(item) for item in d]
        return d

    def reconstruct_enums(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in Varmeinstallation.__members__:
                    d[k] = Varmeinstallation(v)
                elif k in YdervæggensMateriale.__members__:
                    d[k] = YdervæggensMateriale(v)
                elif k in TagdækningsMateriale.__members__:
                    d[k] = TagdækningsMateriale(v)
                elif k in BygningensAnvendelse.__members__:
                    d[k] = BygningensAnvendelse(v)
                elif k in KildeTilBygningensMaterialer.__members__:
                    d[k] = KildeTilBygningensMaterialer(v)
                elif k in SupplerendeVarme.__members__:
                    d[k] = SupplerendeVarme(v)
                elif isinstance(v, list):
                    d[k] = [self.reconstruct_enums(item) for item in v]
                elif isinstance(v, dict):
                    d[k] = self.reconstruct_enums(v)
        elif isinstance(d, list):
            d = [self.reconstruct_enums(item) for item in d]
        return d
