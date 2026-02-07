import pytest_asyncio

from tests.fixtures.product import create_product

TEST_CART_ADD_ITEMS = '/api/v1/cart/items/'


@pytest_asyncio.fixture
async def payload_product():
    products = {
        'mouse': {
            'product_name': 'Mouse',
            'description': 'Мышь для офиса',
            'price': 100,
        },
        'display': {
            'product_name': 'Display',
            'description': 'Игровой монитор',
            'price': 1050,
        },
        'hdmi connector': {
            'product_name': 'HDMI Connector',
            'description': 'HDMI коннектор для PS5>',
            'price': 25,
        },
    }

    return products


@pytest_asyncio.fixture
async def cart_in_db(db_session, payload_product):
    return await create_product(
        db_session,
        products=payload_product,
    )


@pytest_asyncio.fixture
async def cart_out_db(db_session, client, cart_in_db, user_headers):
    resp = await client.post(
        TEST_CART_ADD_ITEMS,
        headers=user_headers,
        json={
            'product_id': cart_in_db[0].product_id,
            'quantity': 1,
        },
    )

    assert resp.status_code == 200, resp.text
    return resp
