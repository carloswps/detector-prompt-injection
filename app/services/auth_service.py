from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repositories.user_repository import UserRepository
from app.services.security_service import (
    get_password_hash,
    create_access_token,
    verify_password,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def register_user(self, user_data):
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_data.password)
        return await self.repository.create_user(user_data.email, hashed_password)

    async def authenticate_user(self, email, password):
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
