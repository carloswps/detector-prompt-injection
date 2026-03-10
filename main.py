import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


knowledge_base = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting ShieldPrompt API...")
    try:
        yield
    except Exception as e:
        logging.error("Erro in lifespan: ", e)
    finally:
        print("🔄 ShieldPrompt API is shutting down...")
        app.state.knowledge_base = None


app = FastAPI(
    title="ShieldPrompt API",
    description="ShieldPrompt API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "message": "ShieldPrompt API is online!"}