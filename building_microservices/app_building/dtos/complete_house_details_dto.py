from pydantic import BaseModel
from .house_details_dto import HouseDetailsDTO

class CompleteHouseDetailsDTO(HouseDetailsDTO):
    seller_info: dict  # In rare cases, this can differ from owner_details
