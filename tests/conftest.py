import os
import pytest_asyncio
import asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from microshop.main import app  # импорт после env!
from microshop.core.models.base import Base
from microshop.core.models.db_helper import db_helper


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(os.environ['DB_URL'], echo=False)

    # Создаём таблицы один раз на сессию тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncSession:
    SessionFactory = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    async with SessionFactory() as session:
        yield session
        # rollback на всякий случай
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    # override dependency
    async def override_get_session():
        yield db_session

    app.dependency_overrides[db_helper.get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac

    app.dependency_overrides.clear()
