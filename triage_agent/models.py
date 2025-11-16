from pydantic import BaseModel

class TriageResult(BaseModel):
    category: str
    priority: int
    account_status: str
    sentiment: str
    confidence: float
    subject: str
    content: str
    requester: str = ''
    recipient: str = ''
