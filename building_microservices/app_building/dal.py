import requests
from shared.database import Database
from models import DamageDetails, BuildingDetails, HouseDetails, OwnerDetails, Hustype, DamageSeverity, CompleteHouseDetails

class BuildingRepository:
    collection = Database.get_collection('houses')

    @staticmethod
    def fetch_address(address: str):
        response = requests.get('https://api.dataforsyningen.dk/autocomplete', params={'q': address, 'type': 'adresse'})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def fetch_address_details(address_id: str):
        response = requests.get(f'https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}')
        response.raise_for_status()
        return response.json()

    @staticmethod
    def fetch_building_details(building_id: str) -> BuildingDetails:
        username = "XJCGPDGQSM"
        password = "$Skole1234"
        params = {
            'id': building_id,
            'username': username,
            'password': password,
        }
        response = requests.get('https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning', params=params)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list):
            data = data[0]  # Return first item if list
        return BuildingDetails(**data)

    @staticmethod
    def fetch_hustype_description(type_id: str):
        # Implement API call or database query to get hustype description
        pass

    @staticmethod
    def fetch_seller_information():
        # Method to fetch seller information based on document structure
        # For now, returning a dummy structure
        return {
            "order_details": {
                "found_by": "family",
                "agent_help": False
            },
            "property_details": {
                "years_owned": 23,
                "residence_period": "since 1997",
                "construction_work": {
                    "additions": False,
                    "renovations": False,
                    "other_buildings": False
                }
            }
        }

    @staticmethod
    def get_full_details(address: str) -> HouseDetails:
        address_data = BuildingRepository.fetch_address(address)
        if not address_data:
            raise ValueError("No address data found")
        address_id = address_data[0]['data']['id']

        address_details = BuildingRepository.fetch_address_details(address_id)
        building_id = address_details[0]['husnummer']['adgangTilBygning']

        building_data = BuildingRepository.fetch_building_details(building_id)
        hustype_data = BuildingRepository.fetch_hustype_description(building_data['building_type'])
        seller_info = BuildingRepository.fetch_seller_information()

        house_details = HouseDetails(
            id=address_id,
            address=address,
            year_built=building_data['year_built'],
            total_area=building_data['area'],
            number_of_buildings=len(building_data.get('additional_buildings', [])) + 1,  # Updated to handle multiple buildings
            main_building_details=BuildingDetails(**building_data),
            additional_buildings=[BuildingDetails(**b) for b in building_data.get('additional_buildings', [])],
            owner_details=OwnerDetails(name="John Doe", contact_information="john.doe@example.com"),
            hustype=Hustype(type_id=building_data['building_type'], **hustype_data),
            wall_conditions=building_data.get('wall_conditions'),
            roof_conditions=building_data.get('roof_conditions'),
            floor_conditions=building_data.get('floor_conditions'),
            windows_doors_conditions=building_data.get('windows_doors_conditions'),
            moisture_mold=building_data.get('moisture_mold'),
            electrical_system=building_data.get('electrical_system'),
            plumbing_system=building_data.get('plumbing_system'),
            heating_system=building_data.get('heating_system'),
            asbestos=building_data.get('asbestos'),
            radon=building_data.get('radon'),
            lead_paint=building_data.get('lead_paint'),
            exterior_walls=building_data.get('exterior_walls'),
            yard_landscaping=building_data.get('yard_landscaping'),
            driveways_walkways=building_data.get('driveways_walkways'),
            interior_rooms=building_data.get('interior_rooms'),
            attic_conditions=building_data.get('attic_conditions'),
            basement_conditions=building_data.get('basement_conditions'),
            insulation=building_data.get('insulation')
        )
        return house_details

    @staticmethod
    def get_complete_house_details(address: str) -> CompleteHouseDetails:
        house_details = BuildingRepository.get_full_details(address)
        seller_info = BuildingRepository.fetch_seller_information()
        complete_house_details = CompleteHouseDetails(**house_details.dict(), seller_info=seller_info)
        return complete_house_details

    # CRUD operations
    @staticmethod
    def create_house_details(house_details: HouseDetails):
        BuildingRepository.collection.insert_one(house_details.dict())

    @staticmethod
    def read_house_details(house_id: str) -> HouseDetails:
        data = BuildingRepository.collection.find_one({"id": house_id})
        if data:
            return HouseDetails(**data)
        return None

    @staticmethod
    def update_house_details(house_id: str, updated_details: dict):
        BuildingRepository.collection.update_one({"id": house_id}, {"$set": updated_details})

    @staticmethod
    def delete_house_details(house_id: str):
        BuildingRepository.collection.delete_one({"id": house_id})