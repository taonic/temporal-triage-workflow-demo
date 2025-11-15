from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    id: str
    title: str
    description: str
    priority: int
    category: str
    source_case_id: str
    created_at: datetime
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    status: str = "open"