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


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class RuleRead(BaseModel):
    id: int
    pattern: str
    rule_type: str
    client_id: str
    user_id: int

    class Config:
        from_attributes = True


class RuleCreate(BaseModel):
    pattern: str
    rule_type: str
    client_id: str
