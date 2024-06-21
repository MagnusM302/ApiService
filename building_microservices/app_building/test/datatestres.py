import os
import sys
import unittest
import requests

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add parent directories to the system path
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
great_grandparent_dir = os.path.dirname(grandparent_dir)

sys.path.append(parent_dir)    # Adding the parent directory to the system path
sys.path.append(grandparent_dir)  # Adding the grandparent directory to the system path
sys.path.append(great_grandparent_dir)  # Adding the great grandparent directory to the system path

from building_microservices.app_building.dal.building_repository import BuildingRepository
from building_microservices.app_building.models import Address, BuildingDetails
from shared.enums import BygningensAnvendelse

class TestBuildingRepository(unittest.TestCase):

    def setUp(self):
        # Set up the test instance of the repository
        self.repository = BuildingRepository()

    def test_fetch_address(self):
        address = "Kærvej 7, 9800"
        result = self.repository.fetch_address(address)
        self.assertIsInstance(result, Address)
        self.assertEqual(result.vejnavn, "Kærvej")
        self.assertEqual(result.husnr, "7")
        self.assertEqual(result.postnr, "9800")
        self.assertIsNotNone(result.id)  # Ensure the ID is present
        print(result)

    def test_fetch_address_details(self):
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"
        result = self.repository.fetch_address_details(address_id)
        self.assertIsInstance(result, Address)
        self.assertEqual(result.id, address_id)
        self.assertEqual(result.vejnavn, "Kærvej")
        self.assertEqual(result.husnr, "7")
        self.assertEqual(result.postnr, "9800")
        print(result)

    def test_fetch_building_details(self):
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        result = self.repository.fetch_building_details(building_id)
        self.assertIsInstance(result, BuildingDetails)
        self.assertEqual(result.id, building_id)
        self.assertEqual(result.byg007Bygningsnummer, 1)  # Assuming '1' is the expected value
        self.assertEqual(result.byg021BygningensAnvendelse.value, '120')  # Correct comparison
        print(result)

if __name__ == '__main__':
    unittest.main()
