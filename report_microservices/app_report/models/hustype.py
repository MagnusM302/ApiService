# models/hustype.py
from pydantic import BaseModel

class Hustype(BaseModel):
    type_id: str
    description: str
