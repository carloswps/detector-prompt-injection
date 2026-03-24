from anyio.functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30

    # Google Gemini
    GOOGLE_GEMINI_API_KEY: str
    GOOGLE_MODEL: str
    HF_TOKEN: str
    HF_API_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
