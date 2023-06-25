import asyncio
import pytest
from main import app
from httpx import AsyncClient

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url='http://test', follow_redirects=True) as client:
        print("Client is ready")
        yield client

@pytest.fixture(scope="session")
async def authenticated_client(token):
    async with AsyncClient(app=app, base_url='http://test', headers={'Authorization': f'Bearer {token}'}, follow_redirects=True) as client:
        print("Client is ready")
        yield client

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()