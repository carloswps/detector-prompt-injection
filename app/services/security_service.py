from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.core import config
from app.core.config import settings

secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
access_token_expire = settings.ACCESS_TOKEN_EXPIRE

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=access_token_expire)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key.encode("utf-8"), algorithm=algorithm)
