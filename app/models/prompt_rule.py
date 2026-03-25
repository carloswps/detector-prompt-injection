from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.prompt_log import Base


class PromptRule(Base):
    __tablename__ = "prompt_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    pattern: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    rule_type: Mapped[str] = mapped_column()
    client_id: Mapped[str | None] = mapped_column(index=True, nullable=True)
