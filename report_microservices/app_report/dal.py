from shared.database import Database
from models import Report
from bson.objectid import ObjectId

class ReportRepository:
    collection = Database.get_collection('reports')

    @staticmethod
    def save(report):
        document = {
            "property_details": report.property_details,
            "owner": report.owner,
            "status": report.status
        }
        if report.report_id is None:
            result = ReportRepository.collection.insert_one(document)
            report.report_id = str(result.inserted_id)
        else:
            ReportRepository.collection.update_one(
                {"_id": ObjectId(report.report_id)},
                {"$set": document}
            )
        return report

    @staticmethod
    def find(report_id):
        doc = ReportRepository.collection.find_one({"_id": ObjectId(report_id)})
        if doc:
            return Report(str(doc['_id']), doc['property_details'], doc['owner'], doc['status'])
        return None

    @staticmethod
    def delete(report_id):
        result = ReportRepository.collection.delete_one({"_id": ObjectId(report_id)})
        return result.deleted_count > 0  # Returnerer True hvis et dokument blev slettet
