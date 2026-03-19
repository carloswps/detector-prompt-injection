import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if GOOGLE_GEMINI_API_KEY is None:
    raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set.")

GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
if GOOGLE_MODEL is None:
    raise ValueError("GOOGLE_MODEL environment variable not set.")

HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable not set.")

HF_API_URL = os.getenv("HF_API_URL")
if HF_API_URL is None:
    raise ValueError("HF_API_URL environment variable not set.")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set.")

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable not set.")

ALGORITHM = os.getenv("ALGORITHM")
if ALGORITHM is None:
    raise ValueError("ALGORITHM environment variable not set.")

ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE")
if ACCESS_TOKEN_EXPIRE is None:
    raise ValueError("ACCESS_TOKEN_EXPIRE environment variable not set.")
ACCESS_TOKEN_EXPIRE = int(ACCESS_TOKEN_EXPIRE)
