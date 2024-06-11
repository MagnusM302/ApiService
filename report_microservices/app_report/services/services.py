from .iservices import IReportService
from ..data.i_report_repository import IReportRepository
from ..dto import CompleteHouseDetailsDTO, OwnerDetailsDTO, AddressDTO, HustypeDTO, ReportBuildingDetailsDTO, CustomerReportDTO
from ..client.building_service_client import BuildingServiceClient
from ..dto.converters import (
    convert_complete_house_details_dto_to_model,
    convert_customer_report_to_dto,
    convert_customer_report_dto_to_model
)
import logging

class ReportService(IReportService):
    def __init__(self, building_service_client: BuildingServiceClient, report_repository: IReportRepository):
        self.building_service_client = building_service_client
        self.report_repository = report_repository

    def generate_report(self, building_id: str = None, address_id: str = None, manual_data: dict = None) -> CompleteHouseDetailsDTO:
        logging.info(f"Generating report for building_id: {building_id} and address_id: {address_id}")
        try:
            if manual_data:
                logging.info("Using manual data for report generation")
                building_details = ReportBuildingDetailsDTO(**manual_data.get("building_details"))
                address_details = AddressDTO(**manual_data.get("address_details"))
            else:
                logging.info("Fetching data from BuildingServiceClient")
                building_details = self.building_service_client.get_building_details(building_id)
                address_details = self.building_service_client.get_address_details(address_id)
            
            if not building_details or not address_details:
                logging.error("Building details or Address details not found")
                return None
            
            owner_details_dto = building_details.owner_details
            hustype_dto = building_details.hustype
            
            complete_house_details_dto = CompleteHouseDetailsDTO(
                **building_details.dict(),
                seller_info=owner_details_dto
            )
            
            report_model = convert_complete_house_details_dto_to_model(complete_house_details_dto)
            self.report_repository.save_report(report_model)
            
            return complete_house_details_dto
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            raise

    def get_report(self, report_id: str) -> CompleteHouseDetailsDTO:
        logging.info(f"Retrieving report with id: {report_id}")
        try:
            report = self.report_repository.get_report(report_id)
            if report:
                return CompleteHouseDetailsDTO.from_model(report)
            else:
                logging.error(f"Report with id: {report_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error retrieving report: {e}")
            raise

    def update_report(self, report_id: str, updated_report: CompleteHouseDetailsDTO):
        logging.info(f"Updating report with id: {report_id}")
        try:
            report_model = convert_complete_house_details_dto_to_model(updated_report)
            self.report_repository.update_report(report_id, report_model)
        except Exception as e:
            logging.error(f"Error updating report: {e}")
            raise

    def delete_report(self, report_id: str):
        logging.info(f"Deleting report with id: {report_id}")
        try:
            self.report_repository.delete_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting report: {e}")
            raise

    def submit_customer_report(self, data: CustomerReportDTO) -> str:
        logging.info("Submitting customer report")
        try:
            customer_report = convert_customer_report_dto_to_model(data)
            self.report_repository.save_customer_report(customer_report)
            return str(customer_report.id)
        except Exception as e:
            logging.error(f"Error submitting customer report: {e}")
            raise

    def create_complete_report(self, customer_report_id: str) -> CompleteHouseDetailsDTO:
        logging.info(f"Creating complete report for customer_report_id: {customer_report_id}")
        try:
            customer_report = self.report_repository.get_customer_report(customer_report_id)
            if not customer_report:
                raise Exception('Customer report not found')

            owner_details_dto = OwnerDetailsDTO(name=customer_report.name, contact_information=customer_report.phone)
            hustype_dto = HustypeDTO(type_id="1", description="Enfamiliehus")

            report_building_details_dto = ReportBuildingDetailsDTO(
                id=customer_report_id,
                address=customer_report.address,
                year_built=customer_report.byggeår,
                number_of_buildings=1,
                owner_details=owner_details_dto,
                hustype=hustype_dto,
                basement_present=True if customer_report.kælder and customer_report.kælder.get('kælder') == 'Ja' else False,
                building_components=[],  # This should be populated with actual data
                varmeinstallation=customer_report.vvs.get('hovedvarmekilde') if customer_report.vvs else None,
                ydervaegsmateriale=None,  # Populate with actual data
                tagdaekningsmateriale=None,  # Populate with actual data
                bygningens_anvendelse=None,  # Populate with actual data
                kilde_til_bygningens_materialer=None,  # Populate with actual data
                supplerende_varme=None,  # Populate with actual data
                remarks=customer_report.bemærkninger
            )

            complete_house_details_dto = CompleteHouseDetailsDTO(
                **report_building_details_dto.dict(),
                seller_info=owner_details_dto
            )

            report_model = convert_complete_house_details_dto_to_model(complete_house_details_dto)
            self.report_repository.save_report(report_model)

            return complete_house_details_dto
        except Exception as e:
            logging.error(f"Error creating complete report: {e}")
            raise

    def delete_customer_report(self, report_id: str):
        logging.info(f"Deleting customer report with id: {report_id}")
        try:
            self.report_repository.delete_customer_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting customer report: {e}")
            raise
