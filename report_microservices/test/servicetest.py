import sys
import os
import unittest
from bson.objectid import ObjectId

# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print(f"sys.path: {sys.path}")

from app_report.services.services import ReportService
from app_report.dto import CompleteHouseDetailsDTO, OwnerDetailsDTO, HustypeDTO, ReportBuildingDetailsDTO
from app_report.dto.converters import convert_complete_house_details_dto_to_model
from report_microservices.app_report.client.building_service_client import BuildingServiceClient
from shared.database import Database


class TestReportService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.building_service_client = BuildingServiceClient(token='YOUR_TOKEN_HERE')
        cls.report_repository = Database.get_collection('reports')
        cls.report_service = ReportService(cls.building_service_client, cls.report_repository)

    def test_generate_report(self):
        building_id = "66659eb1db9f851acaf46dee"  # Existing building ID in the database
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"  # Existing address ID in the database

        report_dto = self.report_service.generate_report(building_id, address_id)

        self.assertIsNotNone(report_dto)
        self.assertEqual(report_dto.year_built, 1990)
        self.assertEqual(report_dto.address, "Main St 123, 12345 City")

        # Check if save_report was called with correct model
        report_model = convert_complete_house_details_dto_to_model(report_dto)
        saved_report = self.report_repository.find_one({'_id': ObjectId(report_model.id)})
        self.assertIsNotNone(saved_report)

    def test_get_report(self):
        report_id = str(ObjectId())
        report_model = {
            "_id": ObjectId(report_id),
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com"
            }
        }
        self.report_repository.insert_one(report_model)

        fetched_report_dto = self.report_service.get_report(report_id)
        self.assertIsNotNone(fetched_report_dto)
        self.assertEqual(fetched_report_dto.id, report_id)
        self.assertEqual(fetched_report_dto.address, "123 Main St")

    def test_update_report(self):
        report_id = str(ObjectId())
        updated_report = CompleteHouseDetailsDTO(
            id=report_id,
            address="123 Main St",
            year_built=1990,
            total_area=150.0,
            number_of_buildings=1,
            owner_details=OwnerDetailsDTO(
                name="John Doe",
                contact_information="john.doe@example.com"
            ),
            hustype=HustypeDTO(
                type_id="1",
                description="Enfamiliehus"
            ),
            basement_present=True,
            building_components=[],
            varmeinstallation="3",
            ydervaegsmateriale="1",
            tagdaekningsmateriale="1",
            bygningens_anvendelse="120",
            kilde_til_bygningens_materialer="Local",
            supplerende_varme="0",
            remarks="Updated remarks",
            seller_info=OwnerDetailsDTO(
                name="Jane Doe",
                contact_information="jane.doe@example.com"
            )
        )

        self.report_service.update_report(report_id, updated_report)

        report_model = convert_complete_house_details_dto_to_model(updated_report)
        updated_report_from_db = self.report_repository.find_one({'_id': ObjectId(report_id)})
        self.assertIsNotNone(updated_report_from_db)
        self.assertEqual(updated_report_from_db['remarks'], "Updated remarks")

    def test_delete_report(self):
        report_id = str(ObjectId())
        report_model = {
            "_id": ObjectId(report_id),
            "address": "123 Main St",
            "year_built": 1990,
            "total_area": 150.0,
            "number_of_buildings": 1,
            "owner_details": {
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            "hustype": {
                "type_id": "1",
                "description": "Enfamiliehus"
            },
            "basement_present": True,
            "building_components": [],
            "varmeinstallation": "3",
            "ydervaegsmateriale": "1",
            "tagdaekningsmateriale": "1",
            "bygningens_anvendelse": "120",
            "kilde_til_bygningens_materialer": "Local",
            "supplerende_varme": "0",
            "remarks": "Some remarks",
            "seller_info": {
                "name": "Jane Doe",
                "contact_information": "jane.doe@example.com"
            }
        }
        self.report_repository.insert_one(report_model)
        self.report_service.delete_report(report_id)
        deleted_report = self.report_repository.find_one({'_id': ObjectId(report_id)})
        self.assertIsNone(deleted_report)

if __name__ == '__main__':
    unittest.main()
