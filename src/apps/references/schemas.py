from typing import List
from pydantic import BaseModel


class Reference(BaseModel):
    id: int
    name: str


class ReferenceData(BaseModel):
    locations: List[Reference]
    genders: List[Reference]
    statuses: List[Reference]
    #  others references
