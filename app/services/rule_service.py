from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.rule_repository import RuleRepository


class RuleService:
    def __init__(self, db_session: AsyncSession):
        self.repo = RuleRepository(db_session)

    async def created_new_rule(
            self, user_id: int, client_id: str, rule_type: str, pattern: str
    ):
        rule = await self.repo.create_rule(
            user_id=user_id, client_id=client_id, rule_type=rule_type, pattern=pattern
        )
        return rule

    async def get_rules_by_client(self, client_id: str):
        return await self.repo.get_rules_by_client_id(client_id=client_id)

    async def delete_rule(self, rule_id: int, user_id: int):
        success = await self.repo.delete_rule(rule_id=rule_id, user_id=user_id)
        if not success:
            raise ValueError("Rule not found or you don't have permission to delete it")
        return success
