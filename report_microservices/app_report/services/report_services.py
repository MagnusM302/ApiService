import logging

from .i_report_services import IReportService
from ..dal.i_report_repository import IReportRepository
from ..dto.complete_house_details_dto import CompleteHouseDetailsDTO
from ..dto.customer_report_dto import CustomerReportDTO
from ..dto.hustype_dto import HustypeDTO
from ..dto.owner_details_dto import OwnerDetailsDTO
from ..dto.inspector_report_dto import InspectorReportDTO
from ..models.customer_report import CustomerReport
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
        print(f"Fetching building details for address: {address}")

    # Step 1: Autocomplete address
        address_details_response = self.building_service_client.get_address_autocomplete(address)
        if not address_details_response or address_details_response.status_code != 200:
            print(f"Failed to autocomplete address. Response: {address_details_response}")
            raise ValueError("Failed to autocomplete address: No results")

        address_details = address_details_response.json()
        print(f"Autocomplete address details: {address_details}")

        if not address_details:
            print("No address details found")
            raise ValueError("Failed to get address details")

        # Step 2: Fetch address details
        address_id = address_details[0]['data']['id']
        print(f"Address ID: {address_id}")

        address_full_details_response = self.building_service_client.get_address_details(address_id)
        if not address_full_details_response or address_full_details_response.status_code != 200:
            print(f"Failed to get address details. Response: {address_full_details_response}")
            raise ValueError("Failed to get address details")

        address_full_details = address_full_details_response.json()
        print(f"Full address details: {address_full_details}")

        building_id = address_full_details.get('building_id', address_id)
        print(f"Building ID: {building_id}")

        # Step 3: Fetch building details
        building_details_response = self.building_service_client.get_building_details(building_id)
        if not building_details_response or building_details_response.status_code != 200:
            print(f"Failed to get building details. Response: {building_details_response}")
            raise ValueError("Failed to get building details")

        building_details = building_details_response.json()
        print(f"Building details: {building_details}")

        # Step 4: Create DTO
        complete_house_details_dto = CompleteHouseDetailsDTO(
            id="generated_id",
            address=address,
            year_built=building_details.get('year_built', 2000),
            total_area=building_details.get('total_area', 100),
            number_of_buildings=building_details.get('number_of_buildings', 1),
            owner_details=OwnerDetailsDTO(
                name="John Doe",
                contact_information="john.doe@example.com",
                period_of_ownership="10 years",
                construction_knowledge="Expert"
            ),
            hustype=HustypeDTO(
                description="Residential",
                type_id="1"
            ),
            varmeinstallation="CENTRAL",
            ydervaegsmateriale="BRICK",
            tagdaekningsmateriale="TILE",
            bygningens_anvendelse="RESIDENTIAL",
            kilde_til_bygningens_materialer="LOCAL",
            supplerende_varme="NONE",
            basement_present=True,
            building_components=[],
            remarks="No remarks",
            inspection_date="2024-01-01",
            inspector_name="Inspector Name",
            inspector_signature="Inspector Signature"
        )

        print(f"Complete house details DTO: {complete_house_details_dto}")
        return complete_house_details_dto

    def generate_inspector_report(self, inspector_report_data: InspectorReportDTO) -> InspectorReportDTO:
        try:
            customer_report = self.report_repository.get_customer_report_by_id(inspector_report_data.customer_report_id)

            if not customer_report:
                raise ValueError("Customer report not found")

            # Fortsæt med behandlingen som krævet
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
            # Convert DTO to model
            customer_report = convert_customer_report_dto_to_model(data)
            # Save the customer report in the repository
            saved_report = self.report_repository.save_customer_report(customer_report)
            # Return the ID of the saved report
            return str(saved_report.id)
        except Exception as e:
            logging.error(f"Error submitting customer report: {e}")
            raise

    def delete_customer_report(self, report_id: str):
        logging.info(f"Deleting customer report with id: {report_id}")
        try:
            # Delete the customer report from the repository
            self.report_repository.delete_customer_report(report_id)
        except Exception as e:
            logging.error(f"Error deleting customer report: {e}")
            raise
