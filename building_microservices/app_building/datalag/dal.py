import requests
import logging
from .interface import IBuildingRepository
from ..models import Address, BuildingDetails
from shared.enums import (
    Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale,
    BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
)
from shared.database import Database

class BuildingRepository(IBuildingRepository):
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.username = "XJCGPDGQSM"
        self.password = "$Skole1234"
        self.address_collection = Database.get_collection('addresses')
        self.building_collection = Database.get_collection('buildings')

    def fetch_address(self, address: str) -> Address:
        existing_address = self.address_collection.find_one({"tekst": address})
        if existing_address:
            return Address(**existing_address)

        logging.info(f"Fetching address for: {address}")
        try:
            params = {'q': address, 'type': 'adresse'}
            response = self.http_client.get('https://api.dataforsyningen.dk/autocomplete', params=params)
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response headers: {response.headers}")
            logging.info(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()
            address_data = response.json()
            logging.info(f"Address Data: {address_data}")
            if not address_data:
                raise ValueError("No address data found")
            data = address_data[0]['data']
            tekst = data.get('tekst', f"{data.get('vejnavn', '')} {data.get('husnr', '')}, {data.get('postnr', '')} {data.get('postnrnavn', '')}")
            new_address = Address(
                id=data.get('id', ''),
                status=data.get('status', ''),
                darstatus=data.get('darstatus', ''),
                vejkode=data.get('vejkode', ''),
                vejnavn=data.get('vejnavn', ''),
                adresseringsvejnavn=data.get('adresseringsvejnavn', ''),
                husnr=data.get('husnr', ''),
                etage=data.get('etage') or '',
                dør=data.get('dør') or '',
                supplerendebynavn=data.get('supplerendebynavn') or '',
                postnr=data.get('postnr', ''),
                postnrnavn=data.get('postnrnavn', ''),
                stormodtagerpostnr=data.get('stormodtagerpostnr') or False,
                stormodtagerpostnrnavn=data.get('stormodtagerpostnrnavn') or '',
                kommunekode=data.get('kommunekode', ''),
                adgangsadresseid=data.get('adgangsadresseid', ''),
                x=data.get('x', None),
                y=data.get('y', None),
                href=data.get('href', ''),
                tekst=tekst
            )
            self.address_collection.insert_one(new_address.dict())
            return new_address
        except requests.RequestException as e:
            logging.error(f"Error fetching address: {e}")
            raise

    def fetch_address_details(self, address_id: str) -> Address:
        existing_address = self.address_collection.find_one({"id": address_id})
        if existing_address:
            return Address(**existing_address)

        logging.info(f"Fetching address details for ID: {address_id}")
        try:
            url = f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}'
            logging.info(f"Request URL: {url}")
            response = self.http_client.get(url)
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response headers: {response.headers}")
            logging.info(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()
            address_details = response.json()
            logging.info(f"Address Details: {address_details}")
            if not address_details:
                raise ValueError(f"No address details found for ID: {address_id}")
            data = address_details[0]
            address_parts = data['adressebetegnelse'].split(',')
            vejnavn_husnr = address_parts[0].strip().split(' ', 1) if len(address_parts) > 0 else ["", ""]
            new_address = Address(
                id=data.get('id_lokalId', ''),
                status=data.get('status', ''),
                darstatus=None,
                vejkode=data.get('vejkode', ''),
                vejnavn=vejnavn_husnr[0] if len(vejnavn_husnr) > 0 else "",
                adresseringsvejnavn=None,
                husnr=vejnavn_husnr[1] if len(vejnavn_husnr) > 1 else "",
                etage=None,
                dør=None,
                supplerendebynavn=None,
                postnr=address_parts[1].strip().split()[0] if len(address_parts) > 1 else "",
                postnrnavn=address_parts[1].strip().split()[1] if len(address_parts) > 1 and len(address_parts[1].strip().split()) > 1 else "",
                stormodtagerpostnr=None,
                stormodtagerpostnrnavn=None,
                kommunekode=None,
                adgangsadresseid=data.get('adgangsadresseid', ''),
                x=None,
                y=None,
                href=None,
                tekst=None
            )
            self.address_collection.insert_one(new_address.dict())
            return new_address
        except requests.RequestException as e:
            logging.error(f"Error fetching address details for ID {address_id}: {e}")
            raise

    def fetch_building_details(self, building_id: str) -> BuildingDetails:
        existing_building = self.building_collection.find_one({"id": building_id})
        if existing_building:
            return BuildingDetails.from_dict(existing_building)

        logging.info(f"Fetching building details for ID: {building_id}")
        try:
            params = {'id': building_id, 'username': self.username, 'password': self.password}
            response = self.http_client.get('https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning', params=params)
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response headers: {response.headers}")
            logging.info(f"Response content: {response.content.decode('utf-8')}")
            response.raise_for_status()
            building_data = response.json()
            logging.info(f"Building Details: {building_data}")
            if not building_data:
                raise ValueError("No building data found")
            data = building_data[0] if isinstance(building_data, list) else building_data
            new_building = BuildingDetails(
                id=data['id_lokalId'],
                byg007Bygningsnummer=data.get('byg007Bygningsnummer'),
                byg021BygningensAnvendelse=BygningensAnvendelse(data.get('byg021BygningensAnvendelse')),
                byg026Opførelsesår=data.get('byg026Opførelsesår'),
                byg032YdervæggensMateriale=YdervæggensMateriale(data.get('byg032YdervæggensMateriale')),
                byg033Tagdækningsmateriale=TagdækningsMateriale(data.get('byg033Tagdækningsmateriale')),
                byg037KildeTilBygningensMaterialer=KildeTilBygningensMaterialer(data.get('byg037KildeTilBygningensMaterialer')),
                byg038SamletBygningsareal=data.get('byg038SamletBygningsareal'),
                byg039BygningensSamledeBoligAreal=data.get('byg039BygningensSamledeBoligAreal'),
                byg041BebyggetAreal=data.get('byg041BebyggetAreal'),
                byg053BygningsarealerKilde=data.get('byg053BygningsarealerKilde'),
                byg054AntalEtager=data.get('byg054AntalEtager'),
                byg056Varmeinstallation=Varmeinstallation(data.get('byg056Varmeinstallation')),
                byg058SupplerendeVarme=SupplerendeVarme(data.get('byg058SupplerendeVarme')),
                byg094Revisionsdato=data.get('byg094Revisionsdato'),
                byg133KildeTilKoordinatsæt=data.get('byg133KildeTilKoordinatsæt'),
                byg134KvalitetAfKoordinatsæt=data.get('byg134KvalitetAfKoordinatsæt'),
                byg135SupplerendeOplysningOmKoordinatsæt=data.get('byg135SupplerendeOplysningOmKoordinatsæt'),
                byg136PlaceringPåSøterritorie=data.get('byg136PlaceringPåSøterritorie'),
                byg404Koordinat=data.get('byg404Koordinat'),
                byg406Koordinatsystem=data.get('byg406Koordinatsystem'),
                forretningshændelse=data.get('forretningshændelse'),
                forretningsområde=data.get('forretningsområde'),
                forretningsproces=data.get('forretningsproces'),
                grund=data.get('grund'),
                husnummer=data.get('husnummer'),
                jordstykke=data.get('jordstykke'),
                kommunekode=data.get('kommunekode'),
                registreringFra=data.get('registreringFra'),
                registreringsaktør=data.get('registreringsaktør'),
                status=data.get('status'),
                virkningFra=data.get('virkningFra'),
                virkningsaktør=data.get('virkningsaktør'),
                etageList=data.get('etageList', []),
                opgangList=data.get('opgangList', [])
            )
            self.building_collection.insert_one(new_building.dict())
            return new_building
        except requests.RequestException as e:
            logging.error(f"Error fetching building details: {e}")
            raise
