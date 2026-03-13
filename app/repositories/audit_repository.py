from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prompt_log import PromptLog


class AuditRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        query = select(PromptLog).order_by(PromptLog.timestamp.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, log_id: int):
        query = select(PromptLog).where(PromptLog.id == log_id)
        result = await self.db.execute(query)
        return result.scalars().first()
