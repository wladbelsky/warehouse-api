import pytest


@pytest.fixture(scope="session")
@pytest.mark.anyio
async def token(client):
    response = await client.post("/api/auth/token/", data={"username": "1", "password": "1"})
    assert response.status_code == 200
    yield response.json().get("access_token")

@pytest.fixture(scope="session")
@pytest.mark.anyio
async def warehouse_id(authenticated_client):
    response = await authenticated_client.post("/api/warehouse/", json={
    "name": "string",
    "address": "string",
    "phone": "string",
    "email": "string"
    })
    assert response.status_code == 200
    yield response.json().get("id")

@pytest.fixture(scope="session")
@pytest.mark.anyio
async def product_id(authenticated_client, warehouse_id):
    response = await authenticated_client.post("/api/product/", json={
    "name": "string",
    "description": "string",
    "price": 0,
    "quantity": 0,
    "warehouse_id": warehouse_id
    })
    assert response.status_code == 200
    yield response.json().get("id")

@pytest.mark.anyio
async def test_token(token):
    assert isinstance(token, str), f"Token is not string, {repr(token)}"
    assert token != "", "Token is empty"

@pytest.mark.anyio
async def test_read_warehouses(authenticated_client):
    response = await authenticated_client.get("/api/warehouse/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_read_warehouse(authenticated_client):
    response = await authenticated_client.get("/api/warehouse/1")
    assert response.status_code == 200
    assert response.json().get("id") == 1

@pytest.mark.anyio
async def test_create_warehouse(warehouse_id):
    assert isinstance(warehouse_id, int) and warehouse_id > 0, f"Warehouse is not int or negative, {repr(warehouse_id)}"

@pytest.mark.anyio
async def test_update_warehouse(authenticated_client, warehouse_id):
    response = await authenticated_client.put(f"/api/warehouse/{warehouse_id}", json={
    "name": "string",
    "address": "string",
    "phone": "string",
    "email": "string"
    })
    assert response.status_code == 200
    assert response.json().get("id") == warehouse_id

@pytest.mark.anyio
async def test_read_products(authenticated_client):
    response = await authenticated_client.get("/api/product/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_read_product(authenticated_client, product_id):
    response = await authenticated_client.get(f"/api/product/{product_id}")
    assert response.status_code == 200
    assert response.json().get("id") == product_id

@pytest.mark.anyio
async def test_create_product(authenticated_client, product_id):
    assert isinstance(product_id, int) and product_id > 0, f"Product is not int or negative, {repr(product_id)}"
    

@pytest.mark.anyio
async def test_update_product(authenticated_client, product_id, warehouse_id):
    response = await authenticated_client.put(f"/api/product/{product_id}", json={
    "name": "string",
    "description": "string",
    "price": 0,
    "quantity": 0,
    "warehouse_id": warehouse_id
    })
    assert response.status_code == 200
    assert response.json().get("id") == product_id

@pytest.mark.anyio
async def test_delete_product(authenticated_client, product_id):
    response = await authenticated_client.delete(f"/api/product/{product_id}")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_delete_warehouse(authenticated_client, warehouse_id):
    response = await authenticated_client.delete(f"/api/warehouse/{warehouse_id}")
    assert response.status_code == 200