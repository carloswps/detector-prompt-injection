from datetime import datetime

from pydantic import BaseModel


class TextPrompt(BaseModel):
    prompt: str


class PromptLogRead(BaseModel):
    id: int
    timestamp: datetime
    prompt: str
    classification: str
    risk_score: float
    is_blocked: bool

    class Config:
        from_attributes = True
