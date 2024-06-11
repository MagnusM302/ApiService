import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import requests

# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../shared')))

from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from building_microservices.app_building.datalag.dal import BuildingRepository
from building_microservices.app_building.models.address import Address
from building_microservices.app_building.models.building_details import BuildingDetails

class TestBuildingRepository(unittest.TestCase):

    @patch('building_microservices.app_building.datalag.dal.Database.get_collection')
    @patch('building_microservices.app_building.datalag.dal.requests.get')
    def test_fetch_building_details(self, mock_requests_get, mock_get_collection):
        # Mock the collection and requests
        mock_building_collection = MagicMock()
        mock_get_collection.return_value = mock_building_collection
        
        # Ensure find_one returns None to simulate no existing data
        mock_building_collection.find_one.return_value = None
        
        # Mock the response data for fetching building details
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        building_data = {
            "id_lokalId": building_id,
            "byg007Bygningsnummer": 1,
            "byg021BygningensAnvendelse": "120",
            "byg026Opførelsesår": 1952,
            "byg032YdervæggensMateriale": "1",
            "byg033Tagdækningsmateriale": "3",
            "byg037KildeTilBygningensMaterialer": "1",
            "byg038SamletBygningsareal": 139,
            "byg039BygningensSamledeBoligAreal": 139,
            "byg041BebyggetAreal": 139,
            "byg053BygningsarealerKilde": "1",
            "byg054AntalEtager": 1,
            "byg056Varmeinstallation": "1",
            "byg058SupplerendeVarme": "5",
            "byg094Revisionsdato": "2017-09-24T09:13:32.432586+02:00",
            "byg133KildeTilKoordinatsæt": "K",
            "byg134KvalitetAfKoordinatsæt": "1",
            "byg135SupplerendeOplysningOmKoordinatsæt": "11",
            "byg136PlaceringPåSøterritorie": "0",
            "byg404Koordinat": "POINT(559435.67 6368107.12)",
            "byg406Koordinatsystem": "5",
            "forretningshændelse": "Bygning",
            "forretningsområde": "54.15.05.05",
            "forretningsproces": "25",
            "etageList": [],
            "opgangList": []
        }
        
        mock_response = MagicMock()
        mock_response.json.return_value = [building_data]
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response
        
        # Initialize the repository
        building_repository = BuildingRepository()

        # Call fetch_building_details and verify the result
        result = building_repository.fetch_building_details(building_id)
        
        # Check if the result matches expected data
        self.assertEqual(result.id, building_id)
        self.assertEqual(result.byg007Bygningsnummer, 1)
        self.assertEqual(result.byg026Opførelsesår, 1952)

        # Verify the data was inserted into the collection
        mock_building_collection.insert_one.assert_called_once()
        inserted_data = mock_building_collection.insert_one.call_args[0][0]
        self.assertEqual(inserted_data['id'], building_id)

    @patch('building_microservices.app_building.datalag.dal.Database.get_collection')
    @patch('building_microservices.app_building.datalag.dal.requests.get')
    def test_fetch_address(self, mock_requests_get, mock_get_collection):
        # Mock the collection and requests
        mock_address_collection = MagicMock()
        mock_get_collection.return_value = mock_address_collection

        # Ensure find_one returns None to simulate no existing data
        mock_address_collection.find_one.return_value = None

        # Mock the response data for fetching address
        address = "Kærvej 7, 9800 Hjørring"
        address_data = [{
            "data": {
                "id": "0a3f50c8-2902-32b8-e044-0003ba298018",
                "status": 1,
                "darstatus": 3,
                "vejkode": "1946",
                "vejnavn": "Kærvej",
                "adresseringsvejnavn": "Kærvej",
                "husnr": "7",
                "etage": "",
                "dør": "",
                "supplerendebynavn": "",
                "postnr": "9800",
                "postnrnavn": "Hjørring",
                "tekst": address,
                "kommunekode": "0860",
                "adgangsadresseid": "0a3f509a-828f-32b8-e044-0003ba298018",
                "x": 9.9904539,
                "y": 57.45180085,
                "href": "https://api.dataforsyningen.dk/adresser/0a3f50c8-2902-32b8-e044-0003ba298018"
            }
        }]

        mock_response = MagicMock()
        mock_response.json.return_value = address_data
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        # Initialize the repository
        building_repository = BuildingRepository()

        # Call fetch_address and verify the result
        result = building_repository.fetch_address(address)

        # Check if the result matches expected data
        self.assertEqual(result.id, "0a3f50c8-2902-32b8-e044-0003ba298018")
        self.assertEqual(result.vejnavn, "Kærvej")
        self.assertEqual(result.postnr, "9800")

        # Verify the data was inserted into the collection
        mock_address_collection.insert_one.assert_called_once()
        inserted_data = mock_address_collection.insert_one.call_args[0][0]
        self.assertEqual(inserted_data['id'], "0a3f50c8-2902-32b8-e044-0003ba298018")

if __name__ == '__main__':
    unittest.main()
