import asyncio
import logging

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.config import settings
from src.app.infrastructure.database.database import Base
from src.app.logger.common import configure_logging
from src.app.main import create_app

configure_logging()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    logger.info("Creating AsyncClient for tests...")
    async with AsyncClient(app=create_app(), base_url="http://test") as ac:
        yield ac


DATABASE_URL = settings.database_url


@pytest.fixture(scope="session")
async def db_engine():
    logger.info("Creating database engine...")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
    logger.info("Database engine disposed.")


@pytest.fixture(scope="function")
async def db_session(db_engine):
    logger.info("Creating new database session...")
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    logger.info("Database session closed.")
