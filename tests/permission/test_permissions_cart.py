import pytest


TEST_CART_ADD_ITEMS = '/api/v1/cart/items/'
TEST_CART_GET_ITEMS = '/api/v1/cart/cart/'


@pytest.mark.asyncio
async def test_cart_for_user_unauthorized(client):
    resp = await client.post(TEST_CART_ADD_ITEMS)
    assert resp.status_code == 401, resp.text


@pytest.mark.asyncio
async def test_cart_get_cart_items(client, user_headers, cart_in_db, cart_out_db):
    resp = await client.get(TEST_CART_GET_ITEMS, headers=user_headers)
    assert resp.status_code == 200

    data = resp.json()
    print(data)
    assert 'cart_id' in data
    assert data['cart_id'] is not None

    assert isinstance(data['items'], list)
    assert len(data['items']) > 0

    item = data['items'][0]
    assert 'product_id' in item
    assert 'quantity' in item
    assert 'unit_price' in item
    assert 'line_total' in item

    assert item['quantity'] == 1
    assert item['line_total'] == item['unit_price'] * item['quantity']

    assert item['line_total'] == sum(i['line_total'] for i in data['items'])
