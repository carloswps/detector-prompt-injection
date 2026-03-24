from typing import Annotated
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.repositories.audit_repository import AuditRepository
from app.schemas.schemas import PromptLogRead, TextPrompt, UserRead
from app.services.ai_service import AIService
from app.services.detector_service import DetectorService

ai_service = AIService()

router = APIRouter(tags=["/analyze"])


@router.post("/analyze", status_code=200)
async def chat(
        request: TextPrompt,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    detector = DetectorService(db)
    result = await detector.analyze_and_log(
        request.prompt, client_id=str(current_user.id), user_id=current_user.id
    )
    return result


@router.get("/history", status_code=200, response_model=List[PromptLogRead])
async def get_history(
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    repo = AuditRepository(db)
    return await repo.get_all()


@router.get("/history/{log_id}", status_code=200, response_model=PromptLogRead)
async def get_history_by_id(
        log_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Annotated[UserRead, Depends(get_current_user)] = None,
):
    repor = AuditRepository(db)
    log = await repor.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
