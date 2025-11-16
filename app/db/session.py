# app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 1. Create the Async Engine
# We use the SYNC URL from settings and just replace the driver
# (or you could add a separate ASYNC_DATABASE_URL to settings)
engine = create_async_engine(
    settings.DATABASE_URL,  # This should be your "postgresql+asyncpg://..."
    echo=True,              # Set to False in production
    future=True
)

# 2. Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# 3. Create the dependency injector
async def get_db() -> AsyncSession:
    """
    FastAPI dependency to get a database session.
    Yields a session and handles closing it.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()