import os
import sys
def set_sys_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(current_dir)
    sys.path.append(parent_dir)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

set_sys_path()

import logging
from shared.enums import Varmeinstallation, YdervæggensMateriale, TagdækningsMateriale, BygningensAnvendelse, KildeTilBygningensMaterialer, SupplerendeVarme
from services.i_report_services import IReportService
from ..dal.i_report_repository import IReportRepository
from ..dto.complete_house_details_dto import CompleteHouseDetailsDTO

from ..dto.customer_report_dto import CustomerReportDTO
from ..dto.inspector_report_dto import InspectorReportDTO
from building_microservices.app_building.dtos.building_details_dto import BuildingDetailsDTO
from building_microservices.app_building.dtos.address_dto import AddressDTO
from ..client.building_service_client import BuildingServiceClient
from ..dto.converters import (
    convert_complete_house_details_dto_to_model,
    convert_customer_report_dto_to_model,
    convert_inspector_report_dto_to_model,
    convert_inspector_report_to_dto,
    convert_customer_report_to_dto
)

class ReportService(IReportService):
    def __init__(self, building_service_client: BuildingServiceClient, report_repository: IReportRepository):
        self.building_service_client = building_service_client
        self.report_repository = report_repository

    def fetch_building_details(self, address: str) -> CompleteHouseDetailsDTO:
        print(f"Fetching address info for address: {address}")
        address_info = self.building_service_client.get_address(address)
        print(f"Address info: {address_info}")
        if address_info is None:
            raise ValueError("Address not found")

        address_id = address_info.adgangsadresseid
        print(f"Address ID: {address_id}")
        address_details = self.building_service_client.get_address_details(address_id)
        print(f"Address details: {address_details}")
        if address_details is None:
            raise ValueError("Address details not found")

        building_id = address_details.adgangsadresseid
        print(f"Building ID: {building_id}")
        building_details = self.building_service_client.get_building_details(building_id)
        print(f"Building details: {building_details}")
        if building_details is None:
            raise ValueError("Building details not found")

        complete_house_details = CompleteHouseDetailsDTO(
            id=building_details.id,
            address=f"{address_details.vejnavn} {address_details.husnr}, {address_details.postnr} {address_details.postnrnavn}",
            year_built=building_details.byg026Opførelsesår,
            total_area=building_details.byg038SamletBygningsareal,
            number_of_buildings=building_details.byg054AntalEtager,
            basement_present=bool(building_details.byg022Kælderareal) if hasattr(building_details, 'byg022Kælderareal') else None,
            varmeinstallation=building_details.byg056Varmeinstallation,
            ydervaegsmateriale=building_details.byg032YdervæggensMateriale,
            tagdaekningsmateriale=building_details.byg033Tagdækningsmateriale,
            bygningens_anvendelse=building_details.byg021BygningensAnvendelse,
            kilde_til_bygningens_materialer=building_details.byg037KildeTilBygningensMaterialer,
            supplerende_varme=building_details.byg058SupplerendeVarme
        )

        return complete_house_details
    
    def generate_inspector_report(self, inspector_report_data: InspectorReportDTO) -> InspectorReportDTO:
        try:
            customer_report = self.report_repository.get_customer_report_by_id(inspector_report_data.customer_report_id)
            if not customer_report:
                raise ValueError("Customer report not found")

            inspector_report = convert_inspector_report_dto_to_model(inspector_report_data)
            self.report_repository.save_inspector_report(inspector_report)

            return inspector_report_data
        except Exception as e:
            logging.error(f"Exception occurred while generating inspector report: {str(e)}")
            raise

    def create_combined_report(self, customer_report_id: str, inspector_report_id: str) -> InspectorReportDTO:
        logging.info(f"Creating combined report for customer_report_id: {customer_report_id} and inspector_report_id: {inspector_report_id}")
        try:
            customer_report = self.report_repository.get_customer_report(customer_report_id)
            inspector_report = self.report_repository.get_inspector_report(inspector_report_id)

            if not customer_report or not inspector_report:
                raise ValueError('Reports not found')

            combined_report = InspectorReportDTO(
                id=inspector_report.id,
                customer_report_id=customer_report_id,
                fetched_building_details=convert_complete_house_details_dto_to_model(inspector_report.fetched_building_details),
                discrepancies=inspector_report.discrepancies,
                inspector_comments=inspector_report.inspector_comments,
                inspection_date=inspector_report.inspection_date,
                inspector_name=inspector_report.inspector_name,
                inspector_signature=inspector_report.inspector_signature,
                building_components=inspector_report.building_components
            )

            self.report_repository.update_inspector_report(inspector_report.id, convert_inspector_report_dto_to_model(combined_report))

            return combined_report
        except Exception as e:
            logging.error(f"Error creating combined report: {e}")
            raise

    def get_inspector_report(self, report_id: str) -> InspectorReportDTO:
        logging.info(f"Retrieving inspector report with id: {report_id}")
        try:
            report = self.report_repository.get_inspector_report(report_id)
            if report:
                return convert_inspector_report_to_dto(report)
            else:
                logging.error(f"Inspector report with id: {report_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error retrieving inspector report: {e}")
            raise

    def update_inspector_report(self, report_id: str, updated_report: InspectorReportDTO):
        logging.info(f"Updating inspector report with id: {report_id}")
        try:
            report_model = convert_inspector_report_dto_to_model(updated_report)
            self.report_repository.update_inspector_report(report_id, report_model)
        except Exception as e:
            logging.error(f"Error updating inspector report: {e}")
            raise

    def delete_inspector_report(self, report_id: str):
        logging.info(f"Deleting inspector report with id: {report_id}")
        try:
            self.report_repository.delete_inspector_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting inspector report: {e}")
            raise

    def submit_customer_report(self, data: CustomerReportDTO) -> str:
        logging.info("Submitting customer report")
        try:
            customer_report = convert_customer_report_dto_to_model(data)
            saved_report = self.report_repository.save_customer_report(customer_report)
            return str(saved_report.id)
        except Exception as e:
            logging.error(f"Error submitting customer report: {e}")
            raise

    def delete_customer_report(self, report_id: str):
        logging.info(f"Deleting customer report with id: {report_id}")
        try:
            self.report_repository.delete_customer_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting customer report: {e}")
            raise
