from fastapi import APIRouter

from app.api.routes import chat, auth

router = APIRouter()

router.include_router(chat.route)
router.include_router(auth.route)
