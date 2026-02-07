import pytest


ADMIN_CREATE_PRODUCT = '/api/v1/admin/product/'


@pytest.mark.asyncio
async def test_admin_endpoint_unauthorized(client):
    resp = await client.post(ADMIN_CREATE_PRODUCT)
    assert resp.status_code == 401, resp.text


@pytest.mark.asyncio
async def test_admin_endpoint_forbidden_for_regular_user(client, user_headers):
    resp = await client.post(ADMIN_CREATE_PRODUCT, headers=user_headers)
    assert resp.status_code == 403, resp.text


@pytest.mark.asyncio
async def test_admin_endpoint_allowed_for_manager(
    client,
    manager_headers,
    grant_for_manager,
):
    await grant_for_manager(['product:create'])
    resp = await client.post(
        ADMIN_CREATE_PRODUCT,
        headers=manager_headers,
        json={
            'product_name': 'Mouse',
            'description': 'Офисная мышь',
            'price': 100,
        },
    )
    assert resp.status_code in (200, 201), resp.text


@pytest.mark.asyncio
async def test_admin_create_product_forbidden_for_user(
    client,
    user_headers,
):
    resp = await client.post(
        ADMIN_CREATE_PRODUCT,
        headers=user_headers,
        json={
            'product_name': 'Mouse',
            'description': 'Офисная мышь',
            'price': 100,
        },
    )
    data = resp.json()
    assert resp.status_code == 403, resp.text
