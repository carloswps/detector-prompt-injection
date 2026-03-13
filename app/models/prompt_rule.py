from sqlalchemy.orm import Mapped, mapped_column

from app.models.prompt_log import Base


class PromptRule(Base):
    __tablename__ = "prompt_rules"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(index=True)
    client_id: Mapped[str | None] = mapped_column(index=True, nullable=True)
    pattern: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
