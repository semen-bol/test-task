from pydantic import BaseModel


class SourceCreated(BaseModel):
    id: int
    name: str

class OperatorLinkedResponse(BaseModel):
    source_id: int
    operator_id: int
    weight: int