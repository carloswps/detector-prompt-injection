import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = os.getenv("HF_API_URL")

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE"))
