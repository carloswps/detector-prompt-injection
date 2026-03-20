from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prompt_log import PromptLog
from app.services.ai_service import AIService


class DetectorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()

    async def analyze_and_log(self, user_text: str, user_id: int):
        injection_score = self.ai_service.get_injection_score(user_text)
        formatted_score = round(injection_score, 4)

        if injection_score > 0.5:
            return await self._block_and_save(
                user_id,
                user_text,
                "Hugging Face Prompt Injection",
                formatted_score,
                "Hugging Face Prompt Injection Detected",
            )

        classification = await self.ai_service.classify_prompt(user_text)

        if classification == "MALICIOUS":
            return await self._block_and_save(
                user_text,
                "Malicious Prompt Detected",
                formatted_score,
                "Malicious Prompt Detected",
            )

        await self._save_log(user_id, user_text, "Safe Prompt", formatted_score, False)

        return {
            "status": "success",
            "message": classification,
            "verification": "Safe",
            "risk_score": formatted_score,
        }

    async def _block_and_save(self, user_id, prompt, category, score, reason):
        await self._save_log(user_id, prompt, category, score, True)
        return {
            "status": "blocked",
            "reason": reason,
            "risk_score": score,
        }

    async def _save_log(self, user_id, prompt, classification, score, blocked):
        new_log = PromptLog(
            user_id=user_id,
            prompt=prompt,
            classification=classification,
            risk_score=score,
            is_blocked=blocked,
        )
        self.db.add(new_log)
        await self.db.commit()
