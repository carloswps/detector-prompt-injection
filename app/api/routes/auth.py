from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import UserCreate
from app.services.auth_service import AuthService

route = APIRouter(tags=["/auth"])


@route.post("/signup", status_code=200)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(user_in)


@route.post("/login", status_code=200)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.authenticate_user(form_data.username, form_data.password)
