from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prompt_log import PromptLog
from app.repositories.rule_repository import RuleRepository
from app.services.ai_service import AIService


class DetectorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()
        self.rule_repo = RuleRepository(db)

    async def analyze_and_log(self, user_text: str, client_id: str, user_id: int):

        rules = await self.rule_repo.get_rules_by_client_id(client_id=client_id)
        formatted_score = 0.0

        if rules:
            rules_list = [f"- Tipo: {r.type}, Padrão: {r.pattern}" for r in rules]
            try:
                violation = await self.ai_service.check_rules_compliance(
                    user_text, rules_list
                )
                if violation and violation.get("is_violation"):
                    return await self._block_and_save(
                        user_id,
                        user_text,
                        f"Context: {violation.get('rule_type')}",
                        1.0,
                        violation.get("reason"),
                    )
            except Exception as e:
                print(f"Erro na análise de compliance: {e}")

        injection_score = self.ai_service.get_injection_score(user_text)
        formatted_score = round(injection_score, 4)

        if injection_score > 0.5:
            return await self._block_and_save(
                user_id,
                user_text,
                "Prompt Injection Detected",
                formatted_score,
                "Possível tentativa de burlar as instruções da IA (Hugging Face Score)",
            )

        await self._save_log(user_id, user_text, "Safe", formatted_score, False)

        return {
            "status": "success",
            "verification": "Passed all security layers",
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
