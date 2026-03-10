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

    if ai_service.is_injection_prompt(user_text):
        return {"status": "blocked", "reason": "Huggin Face Prompt Injection Detected"}

    response = await ai_service.classify_prompt(user_text)
    return {
        "status": "success",
        "message": response,
        "verification": "Safe",
    }
