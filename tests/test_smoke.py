import pytest


@pytest.mark.asyncio
async def test_health(client):
    # если у тебя нет health endpoint — просто дерни любой публичный GET
    resp = await client.get('/api/v1/products/')
    assert resp.status_code in (200, 401, 403, 404)
