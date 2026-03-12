from sqlalchemy.ext.asyncio import AsyncSession

from data.prompt_log import PromptLog


async def save_audit_log(
        db: AsyncSession,
        prompt: str,
        classification: str,
        score: float,
        blocked: bool = False,
):
    new_log = PromptLog(
        prompt=prompt,
        classification=classification,
        risk_score=score,
        is_blocked=blocked,
    )
    db.add(new_log)
    await db.commit()
