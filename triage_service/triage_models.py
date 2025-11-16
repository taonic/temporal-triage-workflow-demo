from pydantic import BaseModel
from typing import Optional

class TriageResult(BaseModel):
    category: str
    priority: int
    account_status: Optional[str] = None
    sentiment: str
    confidence: float
    subject: str
    content: str
    requester: str = ''
    recipient: str = ''
