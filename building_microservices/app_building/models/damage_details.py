from pydantic import BaseModel
from typing import List
from enum import Enum

class DamageSeverity(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"

class DamageDetails(BaseModel):
    description: str
    severity: DamageSeverity
    location: str
