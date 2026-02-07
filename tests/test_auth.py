import pytest
import pytest_asyncio

from microshop.core.models.role import RoleOrm
from microshop.core.models.user import UserOrm
from microshop.api_v1.user.security import hash_password

LOGIN_URL = '/api/v1/auth/login/'
TEST_ME = '/api/v1/auth/me/'
REFRESH_TOKEN = '/api/v1/auth/refresh/'


@pytest.fixture
def user_payload():
    """
    Фикстура с "сырой" информацией пользователя.
    Её удобно переиспользовать в разных тестах (login ok / login fail).
    """
    return {
        'email': 'test_user@example.com',
        'password': '123!',
        'username': 'test_user',
    }


@pytest_asyncio.fixture
async def role_in_db(db_session):
    # Подставь реальные названия полей, если у RoleOrm другие
    role = RoleOrm(
        role_name='user',  # или role_name="user" / title="user"
        # если у роли есть обязательные поля (например description) — добавь их сюда
    )

    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role


@pytest_asyncio.fixture
async def user_in_db(db_session, user_payload, role_in_db):
    """
    Создаёт пользователя в тестовой БД так, как это делает твой реальный код:
    пароль должен быть захэширован.
    """
    user = UserOrm(
        email=user_payload['email'],
        username=user_payload['username'],
        role_id=role_in_db.role_id,
        hashed_password=hash_password(user_payload['password']),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)  # чтобы получить user_id и т.п.

    return user


@pytest_asyncio.fixture
async def auth_tokens(client, user_in_db, user_payload):
    payload = {
        'email': user_payload['email'],
        'password': user_payload['password'],
    }
    resp = await client.post(LOGIN_URL, json=payload)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    access_token = data['access_token']

    refresh_value = resp.cookies.get('refresh_token')
    assert refresh_value is not None

    return {
        'access_token': access_token,
        'refresh_token': refresh_value,
    }


@pytest.mark.asyncio
async def test_login_success(client, user_in_db, user_payload):
    # Arrange
    payload = {
        'email': user_payload['email'],
        'password': user_payload['password'],
    }

    # Act
    resp = await client.post(LOGIN_URL, json=payload)

    # Assert
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert 'access_token' in data
    assert data.get('token_type') in ('bearer', 'Bearer')

    # Проверяем, что refresh_token выставился в cookie
    set_cookie = resp.headers.get('set-cookie', '')
    assert 'refresh_token=' in set_cookie


@pytest.mark.asyncio
async def test_login_wrong_password(client, user_in_db, user_payload):
    payload = {
        'email': user_payload['email'],
        'password': 'wrong_password',
    }

    resp = await client.post(LOGIN_URL, json=payload)
    assert resp.status_code == 401, resp.text

    data = resp.json()
    assert 'access_token' not in data
    set_cookie = resp.headers.get('set-cookie', '')
    assert 'refresh_token=' not in set_cookie


@pytest.mark.asyncio
async def test_login_unknown_email(client, user_in_db, user_payload):
    payload = {
        'email': 'asdf@mail.ru',
        'password': user_payload['password'],
    }

    resp = await client.post(LOGIN_URL, json=payload)
    assert resp.status_code == 401, resp.text

    data = resp.json()
    assert 'access_token' not in data

    set_cookie = resp.headers.get('set-cookie', '')
    assert 'refresh_token' not in set_cookie


@pytest.mark.asyncio
async def test_me_unauthorized(client):
    resp = await client.get(TEST_ME)
    assert resp.status_code == 401, resp.text


@pytest.mark.asyncio
async def test_me_authorized(client, user_in_db, auth_tokens, user_payload):
    headers = {
        'Authorization': f'Bearer {auth_tokens["access_token"]}',
    }
    resp = await client.get(TEST_ME, headers=headers)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert user_payload['email'] == data['email']
    assert user_in_db.user_id == data['user_id']


@pytest.mark.asyncio
async def test_refresh_token(client, user_in_db, auth_tokens):
    resp = await client.post(REFRESH_TOKEN)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert 'access_token' in data


@pytest.mark.asyncio
async def test_refresh_token_wrong(client, user_in_db, auth_tokens):
    client.cookies.set('refresh_token', 'awqefafaf')

    resp = await client.post(REFRESH_TOKEN)
    assert resp.status_code == 401, resp.text
