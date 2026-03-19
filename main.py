import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.core.database import engine
from app.models.prompt_rule import Base

knowledge_base = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Detector Prompt Injection API...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database created")
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
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "online", "message": "ShieldPrompt API is online!"}
