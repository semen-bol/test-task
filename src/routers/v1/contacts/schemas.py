from pydantic import BaseModel
from datetime import datetime


class ContactCreateRequest(BaseModel):
    external_id: str
    source_id: int
    payload: dict | None = None

class ContactResponse(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: int | None
    status: str
    payload: dict | None
    created_at: datetime