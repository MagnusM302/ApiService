#address_processor.py
from typing import Dict
from building_microservices.app_building.dtos.address_dto import AddressDTO
from building_microservices.app_building.models.address import Address

class AddressProcessor:
    @staticmethod
    def process_address_data(address_data: Dict) -> AddressDTO:
        print(f"Processing address data: {address_data}")

        # Ensure 'tekst' field is included if missing
        if 'tekst' not in address_data:
            address_data['tekst'] = f"{address_data.get('vejnavn', '')} {address_data.get('husnr', '')}, {address_data.get('postnr', '')} {address_data.get('postnrnavn', '')}"
        
        # Ensure 'stormodtagerpostnr' is a boolean
        if 'stormodtagerpostnr' not in address_data or address_data['stormodtagerpostnr'] is None:
            address_data['stormodtagerpostnr'] = False
        else:
            address_data['stormodtagerpostnr'] = bool(address_data['stormodtagerpostnr'])

        # Create Address model instance
        address = Address(**address_data)
        
        # Convert Address model to AddressDTO
        address_dto = AddressDTO(
            id=address.id,
            vejkode=address.vejkode,
            vejnavn=address.vejnavn,
            husnr=address.husnr,
            postnr=address.postnr,
            postnrnavn=address.postnrnavn,
            kommunekode=address.kommunekode,
            adgangsadresseid=address.adgangsadresseid,
            tekst=address.tekst
        )
        
        return address_dto
