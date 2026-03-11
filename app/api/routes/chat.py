from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_service import AIService

ai_service = AIService()

route = APIRouter(tags=["/chat"])


class ChatResquest(BaseModel):
    prompt: str


@route.post("/chat")
async def chat(request: ChatResquest):
    user_text = request.prompt

    injection_score = ai_service.get_injection_score(user_text)
    formatted_score = round(injection_score, 4)

    if injection_score > 0.5:
        return {
            "status": "blocked",
            "reason": "Huggin Face Prompt Injection Detected",
            "score": formatted_score,
        }

    response = await ai_service.classify_prompt(user_text)
    if response == "MALICIOUS":
        return {
            "status": "blocked",
            "reason": "Malicious Prompt Detected",
            "risk_score": formatted_score,
        }

    return {
        "status": "success",
        "message": response,
        "verification": "Safe",
        "risk_score": formatted_score,
    }
