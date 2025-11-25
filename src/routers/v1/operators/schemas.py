from pydantic import BaseModel
from datetime import datetime


class ResultOperator(BaseModel):
    id: int
    name: str
    active: bool
    max_leads: int

class CreatedOperator(BaseModel):
    id: int
    name: str
    active: bool
    max_leads: int
    created_at: datetime

