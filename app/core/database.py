from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import config

database_url = config.DATABASE_URL

engine = create_async_engine(database_url, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    """Generator that provides a database session for the routes."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
