import os
from typing import AsyncGenerator

import pytest_asyncio
import asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from microshop.main import app  # импорт после env!
from microshop.core.models.base import Base
from microshop.core.models.db_helper import db_helper
from tests.fixtures.users import create_user
from tests.fixtures.permissions import grant_permissions_to_role, seed_permissions


LOGIN_URL = '/api/v1/auth/login/'


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
async def db_session(test_engine) -> AsyncGenerator[AsyncSession]:
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


@pytest_asyncio.fixture
async def user_payload():
    return {
        'email': 'user1@test.com',
        'password': 'pass123',
        'username': 'user1',
        'role_name': 'user',
    }


@pytest_asyncio.fixture
async def manager_payload():
    return {
        'email': 'manager@test.ru',
        'password': 'manager123',
        'username': 'manager',
        'role_name': 'manager',
    }


@pytest_asyncio.fixture
async def admin_payload():
    return {
        'email': 'admin@mail.ru',
        'password': 'admin123',
        'username': 'Vadim',
        'role_name': 'admin',
    }


@pytest_asyncio.fixture
async def user_in_db(db_session, user_payload):
    return await create_user(
        db_session,
        username=user_payload['username'],
        email=user_payload['email'],
        password=user_payload['password'],
        role_name=user_payload['role_name'],
    )


@pytest_asyncio.fixture
async def manager_in_db(db_session, manager_payload):
    return await create_user(
        db_session,
        username=manager_payload['username'],
        email=manager_payload['email'],
        password=manager_payload['password'],
        role_name=manager_payload['role_name'],
    )


@pytest_asyncio.fixture
async def admin_in_db(db_session, admin_payload):
    return await create_user(
        db_session,
        username=admin_payload['username'],
        email=admin_payload['email'],
        password=admin_payload['password'],
        role_name=admin_payload['role_name'],
    )


@pytest_asyncio.fixture
async def user_headers(client, user_in_db, user_payload):
    resp = await client.post(
        LOGIN_URL,
        json={
            'email': user_payload['email'],
            'password': user_payload['password'],
        },
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def manager_headers(client, manager_in_db, manager_payload):
    resp = await client.post(
        LOGIN_URL,
        json={
            'email': manager_payload['email'],
            'password': manager_payload['password'],
        },
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def admin_headers(client, admin_in_db, admin_payload):
    resp = await client.post(
        LOGIN_URL,
        json={
            'email': admin_payload['email'],
            'password': admin_payload['password'],
        },
    )
    assert resp.status_code == 200, resp.text
    print(resp.json())
    token = resp.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def permissions_map(db_session: AsyncSession):
    return await seed_permissions(db_session=db_session)


@pytest_asyncio.fixture
async def grant_for_manager(db_session: AsyncSession, manager_in_db, permissions_map):
    async def _grant(codes: list[str]):
        return await grant_permissions_to_role(
            db_session=db_session,
            role_id=manager_in_db.role_id,
            codes=codes,
            permissions_map=permissions_map,
        )

    return _grant
