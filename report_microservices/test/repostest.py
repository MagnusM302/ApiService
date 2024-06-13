# report_microservices/test/repostest.py
import sys
import os
import unittest
from bson.objectid import ObjectId

# Tilføj projektets rodmappe til sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

from report_microservices.app_report.models.complete_house_details import CompleteHouseDetails
from report_microservices.app_report.dal.report_repository import ReportRepository
from shared.database import Database

class TestReportRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the specific test database in BuildingReportsDB
        cls.client = Database.client
        cls.db = cls.client['BuildingReportsDB']

        cls.repo = ReportRepository()
        cls.repo.collection = cls.db['reports']  # Ensure we're using the specific test collection

    def setUp(self):
        # Ensure the collection is empty before each test
        self.repo.collection.delete_many({})

    def test_save_report(self):
        report = {
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [
                {
                    "name": "Roof",
                    "condition": "Good",
                    "damage": None,
                    "remarks": None
                }
            ],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            }
        }
        self.repo.collection.insert_one(report)
        saved_report = self.repo.collection.find_one({"address": "123 Main St"})
        self.assertIsNotNone(saved_report)
        self.assertEqual(saved_report['address'], report['address'])
        # Add other assertions based on the fields of CompleteHouseDetails

    def test_get_report(self):
        report = {
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [
                {
                    "name": "Roof",
                    "condition": "Good",
                    "damage": None,
                    "remarks": None
                }
            ],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            }
        }
        insert_result = self.repo.collection.insert_one(report)
        report_id = str(insert_result.inserted_id)
        self.repo.collection.update_one({"_id": ObjectId(report_id)}, {"$set": {"id": report_id}})
        fetched_report = self.repo.get_report(report_id)
        self.assertIsNotNone(fetched_report)
        self.assertEqual(fetched_report.address, report['address'])
        # Add other assertions based on the fields of CompleteHouseDetails

    def test_update_report(self):
        report = {
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [
                {
                    "name": "Roof",
                    "condition": "Good",
                    "damage": None,
                    "remarks": None
                }
            ],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            }
        }
        insert_result = self.repo.collection.insert_one(report)
        report_id = str(insert_result.inserted_id)
        self.repo.collection.update_one({"_id": ObjectId(report_id)}, {"$set": {"id": report_id}})
        updated_report = report.copy()
        updated_report["id"] = report_id
        updated_report["remarks"] = "Updated remarks"
        self.repo.update_report(report_id, CompleteHouseDetails(**updated_report))
        fetched_report = self.repo.get_report(report_id)
        self.assertIsNotNone(fetched_report)
        self.assertEqual(fetched_report.remarks, "Updated remarks")
        # Add other assertions based on the fields of CompleteHouseDetails

    def test_delete_report(self):
        report = {
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [
                {
                    "name": "Roof",
                    "condition": "Good",
                    "damage": None,
                    "remarks": None
                }
            ],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com",
                "period_of_ownership": None,
                "construction_knowledge": None
            }
        }
        insert_result = self.repo.collection.insert_one(report)
        report_id = str(insert_result.inserted_id)
        self.repo.collection.update_one({"_id": ObjectId(report_id)}, {"$set": {"id": report_id}})
        self.repo.delete_report(report_id)
        fetched_report = self.repo.get_report(report_id)
        self.assertIsNone(fetched_report)

if __name__ == '__main__':
    unittest.main()
