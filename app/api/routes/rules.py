from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.repositories.rule_repository import RuleRepository
from app.schemas.schemas import UserRead

route = APIRouter(tags=["/rules"])


@route.post("/rules", status_code=200)
async def create_new_rule(
        pattern: str,
        rule_type: str,
        client_id: str,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    repository = RuleRepository(db)
    rule = await repository.create_rule(
        user_id=current_user.id,
        client_id=client_id,
        rule_type=rule_type,
        pattern=pattern,
    )
    return {"status": "success", "rule_id": rule.id}


@route.get("/rules", status_code=200)
async def list_rules(
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    repository = RuleRepository(db)
    rules = await repository.get_rules_by_client_id(client_id=current_user.id)
    return rules


@route.delete("/rules/{rule_id}", status_code=200)
async def delete_rule(
        rule_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    repository = RuleRepository(db)
    await repository.delete_rule(rule_id)
    return {"status": "success"}
