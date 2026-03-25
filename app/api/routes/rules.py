from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.repositories.rule_repository import RuleRepository
from app.schemas.schemas import UserRead, RuleCreate, RuleRead
from app.services.rule_service import RuleService

router = APIRouter(tags=["Rules"])


@router.post("/", response_model=RuleRead, status_code=200)
async def create_new_rule(
        rule_in: RuleCreate,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    service = RuleService(db)
    return await service.created_new_rule(
        user_id=current_user.id,
        client_id=rule_in.client_id,
        rule_type=rule_in.rule_type,
        pattern=rule_in.pattern,
    )


@router.get("/", status_code=200)
async def list_rules(
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    rules = await RuleRepository(db).get_rules_by_client_id(
        client_id=str(current_user.id)
    )
    return rules


@router.delete("/{rule_id}", status_code=200)
async def delete_rule(
        rule_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    result = await RuleService(db).delete_rule(rule_id, current_user.id)
    if result is None:
        raise ValueError("Rule not found or you don't have permission to delete it")
    return result
