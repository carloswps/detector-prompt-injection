from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.core import config

secret_key = config.SECRET_KEY
algorithm = config.ALGORITHM
access_token_expire = config.ACCESS_TOKEN_EXPIRE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=access_token_expire)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)
