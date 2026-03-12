from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai_service import AIService
from app.services.audit_log import save_audit_log
from data.database import get_db

ai_service = AIService()

route = APIRouter(tags=["/chat"])


class ChatResquest(BaseModel):
    prompt: str


@route.post("/chat")
async def chat(request: ChatResquest, db: AsyncSession = Depends(get_db)):
    user_text = request.prompt

    injection_score = ai_service.get_injection_score(user_text)
    formatted_score = round(injection_score, 4)

    if injection_score > 0.5:
        await save_audit_log(
            db=db,
            prompt=user_text,
            classification="Huggin Face Prompt Injection",
            score=injection_score,
            blocked=True,
        )
        return {
            "status": "blocked",
            "reason": "Huggin Face Prompt Injection Detected",
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
