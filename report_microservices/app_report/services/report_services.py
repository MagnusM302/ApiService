from .i_report_services import IReportService
from ..dal.i_report_repository import IReportRepository
from ..dto import CompleteHouseDetailsDTO, CustomerReportDTO
from ..client.building_service_client import BuildingServiceClient
from ..dto.converters import (
    convert_complete_house_details_dto_to_model,
    convert_customer_report_dto_to_model
)
import logging

class ReportService(IReportService):
    def __init__(self, building_service_client: BuildingServiceClient, report_repository: IReportRepository):
        self.building_service_client = building_service_client
        self.report_repository = report_repository

    def generate_report(self, address: str) -> CompleteHouseDetailsDTO:
        print(f"Generating report for address: {address}")
        try:
            # Step 1: Autocomplete address to get address ID
            address_autocomplete_results = self.building_service_client.get_address_autocomplete(address)
            if not address_autocomplete_results:
                print("Failed to autocomplete address: No results")
                return None

            # Assume the first result is the most relevant
            address_info = address_autocomplete_results.json()[0].get('data', {})
            address_id = address_info.get('id')
            if not address_id:
                print("Address ID not found in autocomplete results")
                return None

            # Step 2: Get detailed address information
            address_details_response = self.building_service_client.get_address_details(address_id)
            if not address_details_response:
                print("Failed to get detailed address information")
                return None

            address_details = address_details_response.json()

            # Step 3: Extract building ID from address details and get building information
            building_id = address_details.get('building_id')
            if not building_id:
                print("Building ID not found in address details")
                return None

            building_details_response = self.building_service_client.get_building_details(building_id)
            if not building_details_response:
                print("Failed to get building details")
                return None

            building_details = building_details_response.json()

            complete_house_details_dto = CompleteHouseDetailsDTO(
                **building_details,
                address=address_details
            )

            report_model = convert_complete_house_details_dto_to_model(complete_house_details_dto)
            self.report_repository.save_report(report_model)

            return complete_house_details_dto
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            raise

    def create_complete_report(self, customer_report_id: str) -> CompleteHouseDetailsDTO:
        logging.info(f"Creating complete report for customer_report_id: {customer_report_id}")
        try:
            customer_report = self.report_repository.get_customer_report(customer_report_id)
            if not customer_report:
                raise ValueError('Customer report not found')

            complete_house_details_dto = CompleteHouseDetailsDTO(
                **customer_report.model_dump(),
                address=customer_report.address
            )

            report_model = convert_complete_house_details_dto_to_model(complete_house_details_dto)
            self.report_repository.save_report(report_model)

            return complete_house_details_dto
        except Exception as e:
            logging.error(f"Error creating complete report: {e}")
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

    def delete_customer_report(self, report_id: str):
        logging.info(f"Deleting customer report with id: {report_id}")
        try:
            self.report_repository.delete_customer_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting customer report: {e}")
            raise
