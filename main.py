import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router

knowledge_base = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Starting ShieldPrompt API v0.1.0...")
    try:
        logging.info("✨ ShieldPrompt API is ready to accept requests")
        yield
    except Exception as e:
        logging.error(f"❌ Error during startup: {e}", exc_info=True)
        raise
    finally:
        logging.info("🔄 ShieldPrompt API is shutting down...")
        if hasattr(app.state, "knowledge_base"):
            app.state.knowledge_base = None
        logging.info("👋 Shutdown complete")


app = FastAPI(
    title="ShieldPrompt API",
    description="ShieldPrompt API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
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
