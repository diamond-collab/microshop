import pytest

TEST_CART_ADD_ITEMS = '/api/v1/cart/items/'

ADMIN_GET_ALL_ORDER = '/api/v1/admin/orders/'
GET_ORDER_BA_ADMIN = '/api/v1/admin/orders/{order_id}'
PATCH_ORDER_BA_ADMIN = '/api/v1/admin/orders/{order_id}/status'
CREATE_USER_ORDER = '/api/v1/order/'


@pytest.mark.asyncio
async def test_admin_unauthorized(client):
    resp = await client.get(ADMIN_GET_ALL_ORDER)
    assert resp.status_code == 401, resp.text


@pytest.mark.asyncio
async def test_admin_forbidden_for_regular_user(client, user_headers):
    resp = await client.get(ADMIN_GET_ALL_ORDER, headers=user_headers)
    assert resp.status_code == 403, resp.text


@pytest.mark.asyncio
async def test_admin_orders_allowed_for_admin(client, admin_headers):
    resp = await client.get(ADMIN_GET_ALL_ORDER, headers=admin_headers)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, list)

    if data:
        o = data[0]
        assert 'order_id' in o
        assert 'order_state' in o
        assert 'created_at' in o
        assert isinstance(o['order_id'], int)
        assert isinstance(o['order_state'], str)
        assert isinstance(o['created_at'], str)


@pytest.mark.asyncio
async def test_admin_orders_allowed_for_manager_with_permission(
    client,
    manager_headers,
    user_headers,
    grant_for_manager,
    cart_out_db,
):
    resp = await client.post(CREATE_USER_ORDER, headers=user_headers)
    assert resp.status_code == 200, resp.text

    await grant_for_manager(['order:read_all'])
    resp = await client.get(ADMIN_GET_ALL_ORDER, headers=manager_headers)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, list)
    if data:
        o = data[0]
        assert 'order_id' in o
        assert 'order_state' in o
        assert 'created_at' in o
        assert isinstance(o['order_id'], int)
        assert isinstance(o['order_state'], str)
        assert isinstance(o['created_at'], str)


@pytest.mark.asyncio
async def test_admin_orders_for_get_order_by_id(
    client,
    manager_headers,
    grant_for_manager,
    user_headers,
    cart_out_db,
):
    resp = await client.post(
        CREATE_USER_ORDER,
        headers=user_headers,
    )
    assert resp.status_code == 200, resp.text

    data = resp.json()

    # Basic contract
    assert (
        data['order_id'] == data['order_id']
    )  # order_id is same as itself, redundant but kept for clarity
    order_id = data['order_id']
    assert 'order_state' in data
    assert 'created_at' in data
    assert 'items' in data
    assert 'total_price' in data

    assert isinstance(data['order_id'], int)
    assert isinstance(data['order_state'], str)
    assert isinstance(data['created_at'], str)
    assert isinstance(data['items'], list)
    assert isinstance(data['total_price'], int)

    # Item contract + math
    if data['items']:
        it = data['items'][0]
        assert 'product_id' in it
        assert 'quantity' in it
        assert 'unit_price' in it
        assert 'line_total' in it

        assert isinstance(it['product_id'], int)
        assert isinstance(it['quantity'], int)
        assert isinstance(it['unit_price'], int)
        assert isinstance(it['line_total'], int)

        assert it['quantity'] > 0
        assert it['unit_price'] >= 0
        assert it['line_total'] == it['unit_price'] * it['quantity']

    # Total price must equal the sum of line totals
    assert data['total_price'] == sum(i['line_total'] for i in data['items'])


@pytest.mark.asyncio
async def test_admin_orders_patch_status_order_by_id(
    client,
    user_headers,
    manager_headers,
    grant_for_manager,
    cart_out_db,
):
    resp = await client.post(
        CREATE_USER_ORDER,
        headers=user_headers,
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    order_id = data['order_id']

    await grant_for_manager(['order:status:update'])

    url = PATCH_ORDER_BA_ADMIN.format(order_id=order_id)
    resp = await client.patch(
        url,
        headers=manager_headers,
        json={'order_state': 'paid'},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    # Contract
    assert data['order_id'] == order_id
    assert 'order_state' in data
    assert isinstance(data['order_state'], str)

    # Status update
    assert data['order_state'] == 'paid'
