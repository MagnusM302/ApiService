# app_report/dto/converters.py
from .report_building_details_dto import ReportBuildingDetailsDTO
from .complete_house_details_dto import CompleteHouseDetailsDTO
from .owner_details_dto import OwnerDetailsDTO
from .hustype_dto import HustypeDTO
from .damage_details_dto import DamageDetailsDTO
from .building_component_dto import BuildingComponentDTO
from ..models.report_building_details import ReportBuildingDetails
from ..models.complete_house_details import CompleteHouseDetails
from ..models.owner_details import OwnerDetails
from ..models.hustype import Hustype
from ..models.damage_details import DamageDetails
from ..models.building_component import BuildingComponent
from ..models.customer_report import CustomerReport
from .customer_report_dto import CustomerReportDTO


def convert_owner_details_dto_to_model(dto: OwnerDetailsDTO) -> OwnerDetails:
    return OwnerDetails(
        name=dto.name,
        contact_information=dto.contact_information,
        period_of_ownership=dto.period_of_ownership,
        construction_knowledge=dto.construction_knowledge
    )

def convert_hustype_dto_to_model(dto: HustypeDTO) -> Hustype:
    return Hustype(
        type_id=dto.type_id,
        description=dto.description
    )

def convert_damage_details_dto_to_model(dto: DamageDetailsDTO) -> DamageDetails:
    return DamageDetails(
        description=dto.description,
        severity=dto.severity,
        location=dto.location
    )

def convert_building_component_dto_to_model(dto: BuildingComponentDTO) -> BuildingComponent:
    return BuildingComponent(
        name=dto.name,
        condition=dto.condition,
        damage=convert_damage_details_dto_to_model(dto.damage) if dto.damage else None,
        remarks=dto.remarks
    )

def convert_report_building_details_dto_to_model(dto: ReportBuildingDetailsDTO) -> ReportBuildingDetails:
    return ReportBuildingDetails(
        id=dto.id,
        address=dto.address,
        year_built=dto.year_built,
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

def convert_complete_house_details_dto_to_model(dto: CompleteHouseDetailsDTO) -> CompleteHouseDetails:
    return CompleteHouseDetails(
        **convert_report_building_details_dto_to_model(dto).model_dump(),
        seller_info=convert_owner_details_dto_to_model(dto.seller_info)
    )
def convert_customer_report_to_dto(customer_report: CustomerReport) -> CustomerReportDTO:
    return CustomerReportDTO(
        id=str(customer_report.id),
        name=customer_report.name,
        phone=customer_report.phone,
        email=customer_report.email,
        address=customer_report.address,
        bestilling_oplysninger=customer_report.bestilling_oplysninger,
        ejendomsmægler=customer_report.ejendomsmægler,
        ejer_år=customer_report.ejer_år,
        boet_periode=customer_report.boet_periode,
        tilbygninger=customer_report.tilbygninger,
        ombygninger=customer_report.ombygninger,
        renoveringer=customer_report.renoveringer,
        andre_bygninger=customer_report.andre_bygninger,
        tag=customer_report.tag,
        ydermur=customer_report.ydermur,
        indre_vægge=customer_report.indre_vægge,
        fundamenter=customer_report.fundamenter,
        kælder=customer_report.kælder,
        gulve=customer_report.gulve,
        vinduer_døre=customer_report.vinduer_døre,
        lofter_etageadskillelser=customer_report.lofter_etageadskillelser,
        vådrum=customer_report.vådrum,
        vvs=customer_report.vvs
    )

def convert_customer_report_dto_to_model(dto: CustomerReportDTO) -> CustomerReport:
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