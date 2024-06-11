import sys
import os
import unittest

# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from building_microservices.app_building.datalag.dal import BuildingRepository
from building_microservices.app_building.models.address import Address
from building_microservices.app_building.models.building_details import BuildingDetails

class TestBuildingRepository(unittest.TestCase):

    def setUp(self):
        self.repository = BuildingRepository()

    def test_fetch_address(self):
        # Act
        address = self.repository.fetch_address("Kærvej 7, 9800")

        # Assert
        self.assertIsInstance(address, Address)
        self.assertEqual(address.vejnavn, "Kærvej")
        self.assertEqual(address.husnr, "7")
        self.assertEqual(address.postnr, "9800")
        self.assertEqual(address.postnrnavn, "Hjørring")
        self.assertEqual(address.tekst, "Kærvej 7, 9800 Hjørring")

    def test_fetch_address_details(self):
        # Known valid address ID
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"

        # Act
        address_details = self.repository.fetch_address_details(address_id)

        # Assert
        self.assertIsInstance(address_details, Address)
        self.assertEqual(address_details.id, address_id)
        self.assertEqual(address_details.vejnavn, "Kærvej")
        self.assertEqual(address_details.husnr, "7")
        self.assertEqual(address_details.postnr, "9800")
        self.assertEqual(address_details.postnrnavn, "Hjørring")

    def test_fetch_building_details(self):
        # Known valid building ID
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"

        # Act
        building_details = self.repository.fetch_building_details(building_id)

        # Assert
        self.assertIsInstance(building_details, BuildingDetails)
        self.assertEqual(building_details.id, building_id)
        self.assertEqual(building_details.byg007Bygningsnummer, 1)
        self.assertEqual(building_details.byg021BygningensAnvendelse.value, "120")
        self.assertEqual(building_details.byg026Opførelsesår, 1952)
        self.assertEqual(building_details.byg032YdervæggensMateriale.value, "1")
        self.assertEqual(building_details.byg033Tagdækningsmateriale.value, "3")
        self.assertEqual(building_details.byg037KildeTilBygningensMaterialer.value, "1")
        self.assertEqual(building_details.byg038SamletBygningsareal, 139)
        self.assertEqual(building_details.byg039BygningensSamledeBoligAreal, 139)
        self.assertEqual(building_details.byg041BebyggetAreal, 139)
        self.assertEqual(building_details.byg053BygningsarealerKilde, "1")
        self.assertEqual(building_details.byg054AntalEtager, 1)
        self.assertEqual(building_details.byg056Varmeinstallation.value, "1")
        self.assertEqual(building_details.byg058SupplerendeVarme.value, "5")
        self.assertEqual(building_details.byg094Revisionsdato, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details.byg133KildeTilKoordinatsæt, "K")
        self.assertEqual(building_details.byg134KvalitetAfKoordinatsæt, "1")
        self.assertEqual(building_details.byg135SupplerendeOplysningOmKoordinatsæt, "11")
        self.assertEqual(building_details.byg136PlaceringPåSøterritorie, "0")
        self.assertEqual(building_details.byg404Koordinat, "POINT(559435.67 6368107.12)")
        self.assertEqual(building_details.byg406Koordinatsystem, "5")
        self.assertEqual(building_details.forretningshændelse, "Bygning")
        self.assertEqual(building_details.forretningsområde, "54.15.05.05")
        self.assertEqual(building_details.forretningsproces, "25")
        self.assertEqual(building_details.grund, "8bd15ce3-07be-4ec1-bd7a-c68b5917ca10")
        self.assertEqual(building_details.husnummer, "0a3f509a-828f-32b8-e044-0003ba298018")
        self.assertEqual(building_details.jordstykke, "1372860")
        self.assertEqual(building_details.kommunekode, "0860")
        self.assertEqual(building_details.registreringFra, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details.registreringsaktør, "BBR")
        self.assertEqual(building_details.status, "6")
        self.assertEqual(building_details.virkningFra, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details.virkningsaktør, "EksterntSystem")

if __name__ == '__main__':
    unittest.main()
