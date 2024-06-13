import sys
import os
import unittest

# Add the root directory of the project to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from building_microservices.app_building.services.building_service import BuildingService
from building_microservices.app_building.dal.building_repository import BuildingRepository
from building_microservices.app_building.models.address import Address
from building_microservices.app_building.models.building_details import BuildingDetails
from building_microservices.app_building.dtos.address_dto import AddressDTO
from building_microservices.app_building.dtos.building_details_dto import BuildingDetailsDTO

class TestBuildingService(unittest.TestCase):

    def setUp(self):
        self.repository = BuildingRepository()
        self.service = BuildingService(self.repository)

    def test_get_address(self):
        address_str = "Kærvej 7, 9800"
        address_dto = self.service.get_address(address_str)

        self.assertIsInstance(address_dto, AddressDTO)
        self.assertEqual(address_dto.vejnavn, "Kærvej")
        self.assertEqual(address_dto.husnr, "7")
        self.assertEqual(address_dto.postnr, "9800")
        self.assertEqual(address_dto.postnrnavn, "Hjørring")
        self.assertEqual(address_dto.tekst, "Kærvej 7, 9800 Hjørring")

    def test_get_address_details(self):
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"
        address_dto = self.service.get_address_details(address_id)

        self.assertIsInstance(address_dto, AddressDTO)
        self.assertEqual(address_dto.id, address_id)
        self.assertEqual(address_dto.vejnavn, "Kærvej")
        self.assertEqual(address_dto.husnr, "7")
        self.assertEqual(address_dto.postnr, "9800")
        self.assertEqual(address_dto.postnrnavn, "Hjørring")

    def test_get_building_details(self):
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        building_details_dto = self.service.get_building_details(building_id)

        self.assertIsInstance(building_details_dto, BuildingDetailsDTO)
        self.assertEqual(building_details_dto.id_lokalId, building_id)
        self.assertEqual(building_details_dto.byg007Bygningsnummer, 1)
        self.assertEqual(building_details_dto.byg021BygningensAnvendelse, "120")
        self.assertEqual(building_details_dto.byg026Opførelsesår, 1952)
        self.assertEqual(building_details_dto.byg032YdervæggensMateriale, "1")
        self.assertEqual(building_details_dto.byg033Tagdækningsmateriale, "3")
        self.assertEqual(building_details_dto.byg037KildeTilBygningensMaterialer, "1")
        self.assertEqual(building_details_dto.byg038SamletBygningsareal, 139)
        self.assertEqual(building_details_dto.byg039BygningensSamledeBoligAreal, 139)
        self.assertEqual(building_details_dto.byg041BebyggetAreal, 139)
        self.assertEqual(building_details_dto.byg053BygningsarealerKilde, "1")
        self.assertEqual(building_details_dto.byg054AntalEtager, 1)
        self.assertEqual(building_details_dto.byg056Varmeinstallation, "1")
        self.assertEqual(building_details_dto.byg058SupplerendeVarme, "5")
        self.assertEqual(building_details_dto.byg094Revisionsdato, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details_dto.byg133KildeTilKoordinatsæt, "K")
        self.assertEqual(building_details_dto.byg134KvalitetAfKoordinatsæt, "1")
        self.assertEqual(building_details_dto.byg135SupplerendeOplysningOmKoordinatsæt, "11")
        self.assertEqual(building_details_dto.byg136PlaceringPåSøterritorie, "0")
        self.assertEqual(building_details_dto.byg404Koordinat, "POINT(559435.67 6368107.12)")
        self.assertEqual(building_details_dto.byg406Koordinatsystem, "5")
        self.assertEqual(building_details_dto.forretningshændelse, "Bygning")
        self.assertEqual(building_details_dto.forretningsområde, "54.15.05.05")
        self.assertEqual(building_details_dto.forretningsproces, "25")
        self.assertEqual(building_details_dto.grund, "8bd15ce3-07be-4ec1-bd7a-c68b5917ca10")
        self.assertEqual(building_details_dto.husnummer, "0a3f509a-828f-32b8-e044-0003ba298018")
        self.assertEqual(building_details_dto.jordstykke, "1372860")
        self.assertEqual(building_details_dto.kommunekode, "0860")
        self.assertEqual(building_details_dto.registreringFra, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details_dto.registreringsaktør, "BBR")
        self.assertEqual(building_details_dto.status, "6")
        self.assertEqual(building_details_dto.virkningFra, "2017-09-24T09:13:32.432586+02:00")
        self.assertEqual(building_details_dto.virkningsaktør, "EksterntSystem")

if __name__ == '__main__':
    unittest.main()
