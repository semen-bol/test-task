from pydantic import BaseModel
from datetime import datetime
from typing import List


class ContactResponse(BaseModel):
    id: int
    source_id: int
    operator_id: int | None
    status: str
    payload: dict | None
    created_at: datetime

class LeadResponse(BaseModel):
    id: int
    external_id: str
    created_at: datetime

class LeadWithContactsResponse(BaseModel):
    lead: LeadResponse
    contacts: List[ContactResponse]