from ..models.address import Address
from .address_dto import AddressDTO
from ..models.building_details import BuildingDetails
from .building_details_dto import BuildingDetailsDTO

def address_to_dto(address: Address) -> AddressDTO:
    return AddressDTO(
        id=address.id,
        vejkode=address.vejkode,
        vejnavn=address.vejnavn,
        adresseringsvejnavn=address.adresseringsvejnavn or "",
        husnr=address.husnr,
        postnr=address.postnr,
        postnrnavn=address.postnrnavn,
        kommunekode=address.kommunekode or "",
        adgangsadresseid=address.adgangsadresseid,
        tekst=address.tekst,
        x=address.x if address.x is not None else 0.0,
        y=address.y if address.y is not None else 0.0,
        href=address.href or "",
        status=address.status,
        darstatus=address.darstatus if address.darstatus is not None else 0,
        stormodtagerpostnr=address.stormodtagerpostnr,
    )

def dto_to_address(dto: AddressDTO) -> Address:
    return Address(
        id=dto.id,
        vejkode=dto.vejkode,
        vejnavn=dto.vejnavn,
        adresseringsvejnavn=dto.adresseringsvejnavn,
        husnr=dto.husnr,
        postnr=dto.postnr,
        postnrnavn=dto.postnrnavn,
        kommunekode=dto.kommunekode,
        adgangsadresseid=dto.adgangsadresseid,
        tekst=dto.tekst,
        x=dto.x,
        y=dto.y,
        href=dto.href,
        status=dto.status,
        darstatus=dto.darstatus,
        stormodtagerpostnr=dto.stormodtagerpostnr,
    )

def building_details_to_dto(details: BuildingDetails) -> BuildingDetailsDTO:
    return BuildingDetailsDTO(
        id=details.id,
        byg007Bygningsnummer=details.byg007Bygningsnummer,
        byg021BygningensAnvendelse=details.byg021BygningensAnvendelse,
        byg026Opførelsesår=details.byg026Opførelsesår,
        byg032YdervæggensMateriale=details.byg032YdervæggensMateriale,
        byg033Tagdækningsmateriale=details.byg033Tagdækningsmateriale,
        byg037KildeTilBygningensMaterialer=details.byg037KildeTilBygningensMaterialer,
        byg038SamletBygningsareal=details.byg038SamletBygningsareal,
        byg039BygningensSamledeBoligAreal=details.byg039BygningensSamledeBoligAreal,
        byg041BebyggetAreal=details.byg041BebyggetAreal,
        byg053BygningsarealerKilde=details.byg053BygningsarealerKilde,
        byg054AntalEtager=details.byg054AntalEtager,
        byg056Varmeinstallation=details.byg056Varmeinstallation,
        byg058SupplerendeVarme=details.byg058SupplerendeVarme,
        byg094Revisionsdato=details.byg094Revisionsdato,
        byg133KildeTilKoordinatsæt=details.byg133KildeTilKoordinatsæt,
        byg134KvalitetAfKoordinatsæt=details.byg134KvalitetAfKoordinatsæt,
        byg135SupplerendeOplysningOmKoordinatsæt=details.byg135SupplerendeOplysningOmKoordinatsæt,
        byg136PlaceringPåSøterritorie=details.byg136PlaceringPåSøterritorie,
        byg404Koordinat=details.byg404Koordinat,
        byg406Koordinatsystem=details.byg406Koordinatsystem,
        forretningshændelse=details.forretningshændelse,
        forretningsområde=details.forretningsområde,
        forretningsproces=details.forretningsproces,
        grund=details.grund,
        husnummer=details.husnummer,
        jordstykke=details.jordstykke,
        kommunekode=details.kommunekode,
        registreringFra=details.registreringFra,
        registreringsaktør=details.registreringsaktør,
        status=details.status,
        virkningFra=details.virkningFra,
        virkningsaktør=details.virkningsaktør,
        etageList=details.etageList,
        opgangList=details.opgangList,
    )

def dto_to_building_details(dto: BuildingDetailsDTO) -> BuildingDetails:
    return BuildingDetails(
        id=dto.id,
        address=dto_to_address(dto.address),
        byg007Bygningsnummer=dto.byg007Bygningsnummer,
        byg021BygningensAnvendelse=dto.byg021BygningensAnvendelse,
        byg026Opførelsesår=dto.byg026Opførelsesår,
        byg032YdervæggensMateriale=dto.byg032YdervæggensMateriale,
        byg033Tagdækningsmateriale=dto.byg033Tagdækningsmateriale,
        byg037KildeTilBygningensMaterialer=dto.byg037KildeTilBygningensMaterialer,
        byg038SamletBygningsareal=dto.byg038SamletBygningsareal,
        byg039BygningensSamledeBoligAreal=dto.byg039BygningensSamledeBoligAreal,
        byg041BebyggetAreal=dto.byg041BebyggetAreal,
        byg053BygningsarealerKilde=dto.byg053BygningsarealerKilde,
        byg054AntalEtager=dto.byg054AntalEtager,
        byg056Varmeinstallation=dto.byg056Varmeinstallation,
        byg058SupplerendeVarme=dto.byg058SupplerendeVarme,
        byg094Revisionsdato=dto.byg094Revisionsdato,
        byg133KildeTilKoordinatsæt=dto.byg133KildeTilKoordinatsæt,
        byg134KvalitetAfKoordinatsæt=dto.byg134KvalitetAfKoordinatsæt,
        byg135SupplerendeOplysningOmKoordinatsæt=dto.byg135SupplerendeOplysningOmKoordinatsæt,
        byg136PlaceringPåSøterritorie=dto.byg136PlaceringPåSøterritorie,
        byg404Koordinat=dto.byg404Koordinat,
        byg406Koordinatsystem=dto.byg406Koordinatsystem,
        status=dto.status,
        virkningFra=dto.virkningFra,
        virkningsaktør=dto.virkningsaktør,
        etageList=dto.etageList,
        opgangList=dto.opgangList,
    )
