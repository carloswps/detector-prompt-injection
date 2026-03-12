from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import TextPrompt, PromptLogRead
from app.services.ai_service import AIService
from app.services.audit_log import save_audit_log
from data.audit_repo import AuditRepository
from data.database import get_db

ai_service = AIService()

route = APIRouter(tags=["/analyze"])


@route.post("/analyze", status_code=200)
async def chat(request: TextPrompt, db: AsyncSession = Depends(get_db)):
    user_text = request.prompt

    injection_score = ai_service.get_injection_score(user_text)
    formatted_score = round(injection_score, 4)

    if injection_score > 0.5:
        await save_audit_log(
            db=db,
            prompt=user_text,
            classification="Hugging Face Prompt Injection",
            score=injection_score,
            blocked=True,
        )
        return {
            "status": "blocked",
            "reason": "Hugging Face Prompt Injection Detected",
            "score": formatted_score,
        }

    response = await ai_service.classify_prompt(user_text)
    if response == "MALICIOUS":
        await save_audit_log(
            db=db,
            prompt=user_text,
            classification="Malicious Prompt Detected",
            score=injection_score,
            blocked=True,
        )

        return {
            "status": "blocked",
            "reason": "Malicious Prompt Detected",
            "risk_score": formatted_score,
        }

    await save_audit_log(
        db=db,
        prompt=user_text,
        classification="Safe Prompt",
        score=injection_score,
        blocked=False,
    )

    return {
        "status": "success",
        "message": response,
        "verification": "Safe",
        "risk_score": formatted_score,
    }


@route.get("/history", status_code=200, response_model=List[PromptLogRead])
async def get_history(db: AsyncSession = Depends(get_db)):
    repo = AuditRepository(db)
    return await repo.get_all()


@route.get("/history/{log_id}", status_code=200, response_model=PromptLogRead)
async def get_history_by_id(log_id: int, db: AsyncSession = Depends(get_db)):
    repor = AuditRepository(db)
    log = await repor.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
