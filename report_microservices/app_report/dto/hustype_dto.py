# hustype_dto.py
from pydantic import BaseModel

class HustypeDTO(BaseModel):
    type_id: str
    description: str
