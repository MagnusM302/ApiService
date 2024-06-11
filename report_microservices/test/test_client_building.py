import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Ensure the root directory of the project is added to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
building_microservices_path = os.path.abspath(os.path.join(project_root, 'ApiService'))

sys.path.insert(0, building_microservices_path)
sys.path.insert(0, project_root)

# Print the current working directory and PYTHONPATH for debugging
print("Current Working Directory:", os.getcwd())
print("PYTHONPATH:", sys.path)

# Import the client and DTOs
from building_microservices.app_building.dtos.address_dto import AddressDTO
from building_microservices.app_building.dtos.building_details_dto import BuildingDetailsDTO
from report_microservices.app_report.client.building_service_client import BuildingServiceClient

class TestBuildingServiceClient(unittest.TestCase):

    def setUp(self):
        self.client = BuildingServiceClient(token="dummy_token")

    @patch('report_microservices.app_report.client.client_building.requests.get')
    def test_get_building_details(self, mock_get):
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        building_data = {
            "id_lokalId": building_id,
            "byg021BygningensAnvendelse": "120",
            "byg056Varmeinstallation": "1",
            "byg032YdervæggensMateriale": "1",
            "byg033Tagdækningsmateriale": "3",
            "byg037KildeTilBygningensMaterialer": "1",
            "byg058SupplerendeVarme": "5",
            "byg007Bygningsnummer": "1",
            "byg026Opførelsesår": 1952,
            "byg038SamletBygningsareal": 139,
            "byg039BygningensSamledeBoligAreal": 139,
            "byg041BebyggetAreal": 139,
            "byg053BygningsarealerKilde": "1",
            "byg054AntalEtager": 1,
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
            "grund": "8bd15ce3-07be-4ec1-bd7a-c68b5917ca10",
            "husnummer": "0a3f509a-828f-32b8-e044-0003ba298018",
            "jordstykke": "1372860",
            "kommunekode": "0860",
            "registreringFra": "2017-09-24T09:13:32.432586+02:00",
            "registreringsaktør": "BBR",
            "status": "6",
            "virkningFra": "2017-09-24T09:13:32.432586+02:00",
            "virkningsaktør": "EksterntSystem"
        }

        mock_response = MagicMock()
        mock_response.json.return_value = building_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        building_details = self.client.get_building_details(building_id)
        self.assertEqual(building_details.id_lokalId, building_id)
        self.assertEqual(building_details.byg021BygningensAnvendelse, "120")

    @patch('report_microservices.app_report.client.client_building.requests.get')
    def test_get_address_details(self, mock_get):
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"
        address_data = {
            "id": address_id,
            "vejkode": "1946",
            "vejnavn": "Kærvej",
            "adresseringsvejnavn": "Kærvej",
            "husnr": "7",
            "postnr": "9800",
            "postnrnavn": "Hjørring",
            "kommunekode": "0860",
            "adgangsadresseid": "0a3f509a-828f-32b8-e044-0003ba298018",
            "x": 9.9904539,
            "y": 57.45180085,
            "href": "https://api.dataforsyningen.dk/adresser/0a3f50c8-2902-32b8-e044-0003ba298018",
            "status": 1,
            "darstatus": 3,
            "tekst": "Kærvej 7, 9800 Hjørring"
        }

        mock_response = MagicMock()
        mock_response.json.return_value = address_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        address_details = self.client.get_address_details(address_id)
        self.assertEqual(address_details.id, address_id)
        self.assertEqual(address_details.vejnavn, "Kærvej")

if __name__ == '__main__':
    unittest.main()
