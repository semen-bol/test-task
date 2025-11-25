from pydantic import BaseModel
from typing import List


class OperatorStats(BaseModel):
    operator_id: int
    operator_name: str
    total_contacts: int
    active_contacts: int
    max_leads: int

class SourceStats(BaseModel):
    source_id: int
    source_name: str
    total_contacts: int

class DistributionStats(BaseModel):
    operator_stats: List[OperatorStats]
    source_stats: List[SourceStats]
    total_leads: int
    total_contacts: int