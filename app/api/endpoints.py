from fastapi import APIRouter

from app.api.routes import chat, auth, rules

router = APIRouter()

router.include_router(chat.route)
router.include_router(auth.route)
router.include_router(rules.route)
