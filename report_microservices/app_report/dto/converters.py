import logging

from .complete_house_details_dto import CompleteHouseDetailsDTO
from .owner_details_dto import OwnerDetailsDTO
from .damage_details_dto import DamageDetailsDTO
from .hustype_dto import HustypeDTO
from .building_component_dto import BuildingComponentDTO

from ..models.complete_house_details import CompleteHouseDetails
from ..models.owner_details import OwnerDetails
from ..models.hustype import Hustype
from ..models.damage_details import DamageDetails
from ..models.building_component import BuildingComponent
from ..models.customer_report import CustomerReport
from .customer_report_dto import CustomerReportDTO
from ..models.inspector_report import InspectorReport
from .inspector_report_dto import InspectorReportDTO

logging.basicConfig(level=logging.DEBUG)

def convert_damage_details_dto_to_model(dto: DamageDetailsDTO) -> DamageDetails:
    return DamageDetails(
        description=dto.description,
        severity=dto.severity,
        location=dto.location,
        remarks=dto.remarks
    )

def convert_damage_details_to_dto(model: DamageDetails) -> DamageDetailsDTO:
    return DamageDetailsDTO(
        description=model.description,
        severity=model.severity,
        location=model.location,
        remarks=model.remarks
    )

def convert_owner_details_dto_to_model(dto: OwnerDetailsDTO) -> OwnerDetails:
    return OwnerDetails(
        name=dto.name,
        contact_information=dto.contact_information,
        period_of_ownership=dto.period_of_ownership,
        construction_knowledge=dto.construction_knowledge
    )

def convert_owner_details_to_dto(model: OwnerDetails) -> OwnerDetailsDTO:
    return OwnerDetailsDTO(
        name=model.name,
        contact_information=model.contact_information,
        period_of_ownership=model.period_of_ownership,
        construction_knowledge=model.construction_knowledge
    )

def convert_hustype_dto_to_model(dto: HustypeDTO) -> Hustype:
    return Hustype(
        type_id=dto.type_id,
        description=dto.description
    )

def convert_hustype_to_dto(model: Hustype) -> HustypeDTO:
    return HustypeDTO(
        type_id=model.type_id,
        description=model.description
    )

def convert_building_component_dto_to_model(dto: BuildingComponentDTO) -> BuildingComponent:
    return BuildingComponent(
        name=dto.name,
        condition=dto.condition,
        damages=[convert_damage_details_dto_to_model(d) for d in dto.damages]
    )

def convert_building_component_to_dto(model: BuildingComponent) -> BuildingComponentDTO:
    return BuildingComponentDTO(
        name=model.name,
        condition=model.condition,
        damages=[convert_damage_details_to_dto(d) for d in model.damages]
    )

def convert_complete_house_details_dto_to_model(dto: CompleteHouseDetailsDTO) -> CompleteHouseDetails:
    return CompleteHouseDetails(
        id=dto.id,
        address=dto.address,
        year_built=str(dto.year_built),
        total_area=dto.total_area,
        number_of_buildings=dto.number_of_buildings,
        owner_details=convert_owner_details_dto_to_model(dto.owner_details),
        hustype=convert_hustype_dto_to_model(dto.hustype),
        basement_present=dto.basement_present,
        building_components=[convert_building_component_dto_to_model(comp) for comp in dto.building_components],
        varmeinstallation=dto.varmeinstallation,
        ydervaegsmateriale=dto.ydervaegsmateriale,
        tagdaekningsmateriale=dto.tagdaekningsmateriale,
        bygningens_anvendelse=dto.bygningens_anvendelse,
        kilde_til_bygningens_materialer=dto.kilde_til_bygningens_materialer,
        supplerende_varme=dto.supplerende_varme,
        remarks=dto.remarks,
        inspection_date=dto.inspection_date,
        inspector_name=dto.inspector_name,
        inspector_signature=dto.inspector_signature
    )

def convert_complete_house_details_to_dto(model: CompleteHouseDetails) -> CompleteHouseDetailsDTO:
    return CompleteHouseDetailsDTO(
        id=model.id,
        address=model.address,
        year_built=str(model.year_built),
        total_area=model.total_area,
        number_of_buildings=model.number_of_buildings,
        owner_details=convert_owner_details_to_dto(model.owner_details),
        hustype=convert_hustype_to_dto(model.hustype),
        basement_present=model.basement_present,
        building_components=[convert_building_component_to_dto(comp) for comp in model.building_components],
        varmeinstallation=model.varmeinstallation,
        ydervaegsmateriale=model.ydervaegsmateriale,
        tagdaekningsmateriale=model.tagdaekningsmateriale,
        bygningens_anvendelse=model.bygningens_anvendelse,
        kilde_til_bygningens_materialer=model.kilde_til_bygningens_materialer,
        supplerende_varme=model.supplerende_varme,
        remarks=model.remarks,
        inspection_date=model.inspection_date,
        inspector_name=model.inspector_name,
        inspector_signature=model.inspector_signature
    )

def convert_inspector_report_dto_to_model(dto: InspectorReportDTO) -> InspectorReport:
    logging.debug(f"Converting InspectorReportDTO to InspectorReport: {dto}")
    return InspectorReport(
        id=dto.id,
        customer_report_id=dto.customer_report_id,
        fetched_building_details=convert_complete_house_details_dto_to_model(dto.fetched_complete_house_details),
        discrepancies=dto.discrepancies,
        inspector_comments=dto.inspector_comments,
        inspection_date=dto.inspection_date,
        inspector_name=dto.inspector_name,
        inspector_signature=dto.inspector_signature,
        building_components=[convert_building_component_dto_to_model(comp) for comp in dto.building_components]
    )


def convert_inspector_report_to_dto(model: InspectorReport) -> InspectorReportDTO:
    logging.debug(f"Converting InspectorReport to InspectorReportDTO: {model}")
    return InspectorReportDTO(
        id=model.id,
        customer_report_id=model.customer_report_id,
        fetched_complete_house_details=convert_complete_house_details_to_dto(model.fetched_building_details),
        discrepancies=model.discrepancies,
        inspector_comments=model.inspector_comments,
        inspection_date=model.inspection_date,
        inspector_name=model.inspector_name,
        inspector_signature=model.inspector_signature,
        building_components=[convert_building_component_to_dto(comp) for comp in model.building_components]
    )



def convert_customer_report_dto_to_model(dto: CustomerReportDTO) -> CustomerReport:
    logging.debug(f"Converting CustomerReportDTO to CustomerReport: {dto}")
    return CustomerReport(
        id=dto.id,
        name=dto.name,
        phone=dto.phone,
        email=dto.email,
        address=dto.address,
        bestilling_oplysninger=dto.bestilling_oplysninger,
        ejendomsmægler=dto.ejendomsmægler,
        ejer_år=dto.ejer_år,
        boet_periode=dto.boet_periode,
        tilbygninger=dto.tilbygninger,
        ombygninger=dto.ombygninger,
        renoveringer=dto.renoveringer,
        andre_bygninger=dto.andre_bygninger,
        tag=dto.tag,
        ydermur=dto.ydermur,
        indre_vægge=dto.indre_vægge,
        fundamenter=dto.fundamenter,
        kælder=dto.kælder,
        gulve=dto.gulve,
        vinduer_døre=dto.vinduer_døre,
        lofter_etageadskillelser=dto.lofter_etageadskillelser,
        vådrum=dto.vådrum,
        vvs=dto.vvs
    )

def convert_customer_report_to_dto(model: CustomerReport) -> CustomerReportDTO:
    logging.debug(f"Converting CustomerReport to CustomerReportDTO: {model}")
    return CustomerReportDTO(
        id=str(model.id),
        name=model.name,
        phone=model.phone,
        email=model.email,
        address=model.address,
        bestilling_oplysninger=model.bestilling_oplysninger,
        ejendomsmægler=model.ejendomsmægler,
        ejer_år=model.ejer_år,
        boet_periode=model.boet_periode,
        tilbygninger=model.tilbygninger,
        ombygninger=model.ombygninger,
        renoveringer=model.renoveringer,
        andre_bygninger=model.andre_bygninger,
        tag=model.tag,
        ydermur=model.ydermur,
        indre_vægge=model.indre_vægge,
        fundamenter=model.fundamenter,
        kælder=model.kælder,
        gulve=model.gulve,
        vinduer_døre=model.vinduer_døre,
        lofter_etageadskillelser=model.lofter_etageadskillelser,
        vådrum=model.vådrum,
        vvs=model.vvs
    )
