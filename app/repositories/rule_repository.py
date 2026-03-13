from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prompt_rule import PromptRule


class RuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_rules_by_client_id(self, client_id: str):
        query = select(PromptRule).where(PromptRule.client_id == client_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_rule(self, client_id: str, rule_type: str, pattern: str):
        rule = PromptRule(client_id=client_id, type=rule_type, pattern=pattern)
        self.db.add(rule)
        await self.db.commit()
        return rule
