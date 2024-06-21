# report_microservices/test/repostest.py
import sys
import os
import unittest

# Tilføj projektets rodmappe til sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

from bson.objectid import ObjectId
from pymongo import MongoClient
from report_microservices.app_report.models.complete_house_details import CompleteHouseDetails
from report_microservices.app_report.models.customer_report import CustomerReport
from report_microservices.app_report.models.inspector_report import InspectorReport
from report_microservices.app_report.dal.report_repository import ReportRepository
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from shared.database import Database

class TestReportRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the specific test database in BuildingReportsDB
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['BuildingReportsDB']
        Database.client = cls.client

        cls.repo = ReportRepository(Database)
        cls.repo.inspector_report_collection = cls.db['inspector_reports']
        cls.repo.customer_report_collection = cls.db['customer_reports']

    def setUp(self):
        # Ensure the collections are empty before each test
        self.repo.inspector_report_collection.delete_many({})
        self.repo.customer_report_collection.delete_many({})

    def test_save_inspector_report(self):
        complete_house_details = CompleteHouseDetails(
            id="generated_id",
            address="123 Main St",
            year_built=1990,
            total_area=150.0,
            number_of_buildings=1,
            owner_details={
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            hustype={
                "description": "Residential",
                "type_id": "1"
            },
            varmeinstallation=Varmeinstallation.GAS,
            ydervaegsmateriale=YdervæggensMateriale.BRICK,
            tagdaekningsmateriale=TagdækningsMateriale.TILE,
            bygningens_anvendelse=BygningensAnvendelse.RESIDENTIAL,
            kilde_til_bygningens_materialer=KildeTilBygningensMaterialer.LOCAL,
            supplerende_varme=SupplerendeVarme.NONE,
            basement_present=True,
            building_components=[],
            remarks="Some remarks",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature"
        )
        
        inspector_report = InspectorReport(
            customer_report_id="customer_report_id",
            fetched_building_details=complete_house_details.model_dump(),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature",
            building_components=[]
        )
        saved_report = self.repo.save_inspector_report(inspector_report)
        self.assertIsNotNone(saved_report.id)
        self.assertEqual(saved_report.customer_report_id, "customer_report_id")

    def test_get_inspector_report(self):
        complete_house_details = CompleteHouseDetails(
            id="generated_id",
            address="123 Main St",
            year_built=1990,
            total_area=150.0,
            number_of_buildings=1,
            owner_details={
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            hustype={
                "description": "Residential",
                "type_id": "1"
            },
            varmeinstallation=Varmeinstallation.GAS,
            ydervaegsmateriale=YdervæggensMateriale.BRICK,
            tagdaekningsmateriale=TagdækningsMateriale.TILE,
            bygningens_anvendelse=BygningensAnvendelse.RESIDENTIAL,
            kilde_til_bygningens_materialer=KildeTilBygningensMaterialer.LOCAL,
            supplerende_varme=SupplerendeVarme.NONE,
            basement_present=True,
            building_components=[],
            remarks="Some remarks",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature"
        )
        
        inspector_report = InspectorReport(
            customer_report_id="customer_report_id",
            fetched_building_details=complete_house_details.model_dump(),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature",
            building_components=[]
        )
        saved_report = self.repo.save_inspector_report(inspector_report)
        fetched_report = self.repo.get_inspector_report(saved_report.id)
        self.assertIsNotNone(fetched_report)
        self.assertEqual(fetched_report.customer_report_id, "customer_report_id")

    def test_update_inspector_report(self):
        complete_house_details = CompleteHouseDetails(
            id="generated_id",
            address="123 Main St",
            year_built=1990,
            total_area=150.0,
            number_of_buildings=1,
            owner_details={
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            hustype={
                "description": "Residential",
                "type_id": "1"
            },
            varmeinstallation=Varmeinstallation.GAS,
            ydervaegsmateriale=YdervæggensMateriale.BRICK,
            tagdaekningsmateriale=TagdækningsMateriale.TILE,
            bygningens_anvendelse=BygningensAnvendelse.RESIDENTIAL,
            kilde_til_bygningens_materialer=KildeTilBygningensMaterialer.LOCAL,
            supplerende_varme=SupplerendeVarme.NONE,
            basement_present=True,
            building_components=[],
            remarks="Some remarks",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature"
        )
        
        inspector_report = InspectorReport(
            customer_report_id="customer_report_id",
            fetched_building_details=complete_house_details.model_dump(),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature",
            building_components=[]
        )
        saved_report = self.repo.save_inspector_report(inspector_report)
        saved_report.inspector_comments = "Updated comments"
        self.repo.update_inspector_report(saved_report.id, saved_report)
        updated_report = self.repo.get_inspector_report(saved_report.id)
        self.assertIsNotNone(updated_report)
        self.assertEqual(updated_report.inspector_comments, "Updated comments")

    def test_delete_inspector_report(self):
        complete_house_details = CompleteHouseDetails(
            id="generated_id",
            address="123 Main St",
            year_built=1990,
            total_area=150.0,
            number_of_buildings=1,
            owner_details={
                "name": "John Doe",
                "contact_information": "john.doe@example.com"
            },
            hustype={
                "description": "Residential",
                "type_id": "1"
            },
            varmeinstallation=Varmeinstallation.GAS,
            ydervaegsmateriale=YdervæggensMateriale.BRICK,
            tagdaekningsmateriale=TagdækningsMateriale.TILE,
            bygningens_anvendelse=BygningensAnvendelse.RESIDENTIAL,
            kilde_til_bygningens_materialer=KildeTilBygningensMaterialer.LOCAL,
            supplerende_varme=SupplerendeVarme.NONE,
            basement_present=True,
            building_components=[],
            remarks="Some remarks",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature"
        )
        
        inspector_report = InspectorReport(
            customer_report_id="customer_report_id",
            fetched_building_details=complete_house_details.model_dump(),
            discrepancies="",
            inspector_comments="No comments",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature",
            building_components=[]
        )
        saved_report = self.repo.save_inspector_report(inspector_report)
        self.repo.delete_inspector_report(saved_report.id)
        fetched_report = self.repo.get_inspector_report(saved_report.id)
        self.assertIsNone(fetched_report)

    def test_save_customer_report(self):
        customer_report = CustomerReport(
            id="generated_id",
            name="Customer Name",
            phone="Customer Contact",
            email="customer@example.com",
            address="123 Main St",
            bestilling_oplysninger="Some details",
            ejendomsmægler="Some real estate agent",
            ejer_år=2024,
            boet_periode="2024-01-01 to 2024-12-31",
            tilbygninger="None",
            ombygninger="None",
            renoveringer="None",
            andre_bygninger="None",
            tag={"description": "Good condition"},
            ydermur={"description": "Good condition"},
            indre_vægge={"description": "Good condition"},
            fundamenter={"description": "Good condition"},
            kælder={"description": "Good condition"},
            gulve={"description": "Good condition"},
            vinduer_døre={"description": "Good condition"},
            lofter_etageadskillelser={"description": "Good condition"},
            vådrum={"description": "Good condition"},
            vvs={"description": "Good condition"}
        )
        saved_report = self.repo.save_customer_report(customer_report)
        self.assertIsNotNone(saved_report.id)
        self.assertEqual(saved_report.address, "123 Main St")

    def test_get_customer_report(self):
        customer_report = CustomerReport(
            id="generated_id",
            name="Customer Name",
            phone="Customer Contact",
            email="customer@example.com",
            address="123 Main St",
            bestilling_oplysninger="Some details",
            ejendomsmægler="Some real estate agent",
            ejer_år=2024,
            boet_periode="2024-01-01 to 2024-12-31",
            tilbygninger="None",
            ombygninger="None",
            renoveringer="None",
            andre_bygninger="None",
            tag={"description": "Good condition"},
            ydermur={"description": "Good condition"},
            indre_vægge={"description": "Good condition"},
            fundamenter={"description": "Good condition"},
            kælder={"description": "Good condition"},
            gulve={"description": "Good condition"},
            vinduer_døre={"description": "Good condition"},
            lofter_etageadskillelser={"description": "Good condition"},
            vådrum={"description": "Good condition"},
            vvs={"description": "Good condition"}
        )
        saved_report = self.repo.save_customer_report(customer_report)
        fetched_report = self.repo.get_customer_report(saved_report.id)
        self.assertIsNotNone(fetched_report)
        self.assertEqual(fetched_report.address, "123 Main St")

    def test_update_customer_report(self):
        customer_report = CustomerReport(
            id="generated_id",
            name="Customer Name",
            phone="Customer Contact",
            email="customer@example.com",
            address="123 Main St",
            bestilling_oplysninger="Some details",
            ejendomsmægler="Some real estate agent",
            ejer_år=2024,
            boet_periode="2024-01-01 to 2024-12-31",
            tilbygninger="None",
            ombygninger="None",
            renoveringer="None",
            andre_bygninger="None",
            tag={"description": "Good condition"},
            ydermur={"description": "Good condition"},
            indre_vægge={"description": "Good condition"},
            fundamenter={"description": "Good condition"},
            kælder={"description": "Good condition"},
            gulve={"description": "Good condition"},
            vinduer_døre={"description": "Good condition"},
            lofter_etageadskillelser={"description": "Good condition"},
            vådrum={"description": "Good condition"},
            vvs={"description": "Good condition"}
        )
        saved_report = self.repo.save_customer_report(customer_report)
        saved_report.bestilling_oplysninger = "Updated details"
        self.repo.update_customer_report(saved_report.id, saved_report)
        updated_report = self.repo.get_customer_report(saved_report.id)
        self.assertIsNotNone(updated_report)
        self.assertEqual(updated_report.bestilling_oplysninger, "Updated details")

    def test_delete_customer_report(self):
        customer_report = CustomerReport(
            id="generated_id",
            name="Customer Name",
            phone="Customer Contact",
            email="customer@example.com",
            address="123 Main St",
            bestilling_oplysninger="Some details",
            ejendomsmægler="Some real estate agent",
            ejer_år=2024,
            boet_periode="2024-01-01 to 2024-12-31",
            tilbygninger="None",
            ombygninger="None",
            renoveringer="None",
            andre_bygninger="None",
            tag={"description": "Good condition"},
            ydermur={"description": "Good condition"},
            indre_vægge={"description": "Good condition"},
            fundamenter={"description": "Good condition"},
            kælder={"description": "Good condition"},
            gulve={"description": "Good condition"},
            vinduer_døre={"description": "Good condition"},
            lofter_etageadskillelser={"description": "Good condition"},
            vådrum={"description": "Good condition"},
            vvs={"description": "Good condition"}
        )
        saved_report = self.repo.save_customer_report(customer_report)
        self.repo.delete_customer_report(saved_report.id)
        fetched_report = self.repo.get_customer_report(saved_report.id)
        self.assertIsNone(fetched_report)

if __name__ == '__main__':
    unittest.main()
