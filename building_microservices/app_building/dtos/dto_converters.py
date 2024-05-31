from building_microservices.app_building.models import Address, BuildingDetails, HouseDetails, CompleteHouseDetails, Hustype, OwnerDetails
from building_microservices.app_building.dtos import AddressDTO, BuildingDetailsDTO, HouseDetailsDTO, CompleteHouseDetailsDTO

class DTOConverters:
    
    
    @staticmethod
    def to_address_dto(address: Address) -> AddressDTO:
        print(f"Converting to AddressDTO with data: {address}")
        
        # Fallback for tekst field if it is missing
        if not address.tekst:
            address.tekst = f"{address.vejnavn} {address.husnr}, {address.postnr} {address.postnrnavn}"
        
        return AddressDTO(
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
    
    @staticmethod
    def from_dict(data: dict) -> Address:
        # Ensure 'tekst' field is included if missing
        if 'tekst' not in data:
            data['tekst'] = f"{data.get('vejnavn', '')} {data.get('husnr', '')}, {data.get('postnr', '')} {data.get('postnrnavn', '')}"
        
        # Ensure 'stormodtagerpostnr' is a boolean
        if 'stormodtagerpostnr' not in data or data['stormodtagerpostnr'] is None:
            data['stormodtagerpostnr'] = False

        return Address(**data)

    @staticmethod
    def to_building_details_dto(building_details: BuildingDetails) -> BuildingDetailsDTO:
        return BuildingDetailsDTO(
            id=building_details.id,
            year_built=building_details.year_built,
            area=building_details.area,
            rooms=building_details.rooms,
            condition=building_details.condition,
            wall_conditions=building_details.wall_conditions,
            roof_conditions=building_details.roof_conditions,
            floor_conditions=building_details.floor_conditions,
            windows_doors_conditions=building_details.windows_doors_conditions,
            moisture_mold=building_details.moisture_mold,
            electrical_system=building_details.electrical_system,
            plumbing_system=building_details.plumbing_system,
            heating_system=building_details.heating_system,
            asbestos=building_details.asbestos,
            radon=building_details.radon,
            lead_paint=building_details.lead_paint,
            exterior_walls=building_details.exterior_walls,
            yard_landscaping=building_details.yard_landscaping,
            driveways_walkways=building_details.driveways_walkways,
            interior_rooms=building_details.interior_rooms,
            attic_conditions=building_details.attic_conditions,
            basement_conditions=building_details.basement_conditions,
            insulation=building_details.insulation
        )

    @staticmethod
    def to_house_details_dto(house_details: HouseDetails) -> HouseDetailsDTO:
        return HouseDetailsDTO(
            id=house_details.id,
            address=house_details.address,
            year_built=house_details.year_built,
            total_area=house_details.total_area,
            number_of_buildings=house_details.number_of_buildings,
            main_building_details=DTOConverters.to_building_details_dto(house_details.main_building_details),
            additional_buildings=[DTOConverters.to_building_details_dto(b) for b in house_details.additional_buildings],
            owner_details=house_details.owner_details.dict(),
            hustype=house_details.hustype.dict()
        )

    @staticmethod
    def to_complete_house_details_dto(complete_house_details: CompleteHouseDetails) -> CompleteHouseDetailsDTO:
        return CompleteHouseDetailsDTO(
            **DTOConverters.to_house_details_dto(complete_house_details).dict(),
            seller_info=complete_house_details.seller_info.dict()
        )

    @staticmethod
    def to_house_details(house_details_dto: HouseDetailsDTO) -> HouseDetails:
        return HouseDetails(
            id=house_details_dto.id,
            address=house_details_dto.address,
            year_built=house_details_dto.year_built,
            total_area=house_details_dto.total_area,
            number_of_buildings=house_details_dto.number_of_buildings,
            main_building_details=BuildingDetails(**house_details_dto.main_building_details.dict()),
            additional_buildings=[BuildingDetails(**b.dict()) for b in house_details_dto.additional_buildings],
            owner_details=OwnerDetails(**house_details_dto.owner_details),
            hustype=Hustype(**house_details_dto.hustype)
        )
