from typing import Optional
from ..models.complete_house_details import CompleteHouseDetails
from bson.objectid import ObjectId
from .i_report_repository import IReportRepository
from enum import Enum
from ..models.customer_report import CustomerReport
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from shared.database import Database

class ReportRepository(IReportRepository):
    def __init__(self, db: Database):
        self.collection = db.get_collection('reports')
        self.customer_report_collection = db.get_collection('customer_reports')
    

    def save_report(self, report: CompleteHouseDetails):
        report_dict = report.model_dump()
        report_dict = self.convert_enums(report_dict)
        self.collection.insert_one(report_dict)

    def get_report(self, report_id: str) -> Optional[CompleteHouseDetails]:
        report_data = self.collection.find_one({"_id": ObjectId(report_id)})
        if report_data:
            report_data = self.reconstruct_enums(report_data)
            return CompleteHouseDetails(**report_data)
        return None

    def update_report(self, report_id: str, report: CompleteHouseDetails):
        report_dict = report.model_dump()
        report_dict = self.convert_enums(report_dict)
        self.collection.update_one({"_id": ObjectId(report_id)}, {"$set": report_dict})

    def delete_report(self, report_id: str):
        self.collection.delete_one({"_id": ObjectId(report_id)})
    
    def save_customer_report(self, customer_report: CustomerReport):
        customer_report_dict = customer_report.model_dump()
        self.customer_report_collection.insert_one(customer_report_dict)

    def get_customer_report(self, report_id: str) -> Optional[CustomerReport]:
        customer_report_data = self.customer_report_collection.find_one({"_id": ObjectId(report_id)})
        if customer_report_data:
            return CustomerReport(**customer_report_data)
        return None
    
    def delete_customer_report(self, report_id: str):
        self.customer_report_collection.delete_one({"_id": ObjectId(report_id)})

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
