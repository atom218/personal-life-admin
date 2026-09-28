from pydantic import BaseModel
from typing import Optional


class ExtractedTask(BaseModel):
    actionable: bool
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: str
    category: Optional[str] = None
    confidence: float