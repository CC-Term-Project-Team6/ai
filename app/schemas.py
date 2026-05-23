from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    request_id: str
    text: str


class AnalyzeResponse(BaseModel):
    request_id: str
    label: str
    risk_level: str
    confidence: float
    reason: List[str]