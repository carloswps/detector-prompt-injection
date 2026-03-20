from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class PromptLog(Base):
    __tablename__ = "prompt_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    prompt: Mapped[str] = mapped_column()
    classification: Mapped[str] = mapped_column()
    risk_score: Mapped[float] = mapped_column()
    is_blocked: Mapped[bool] = mapped_column(default=False)
