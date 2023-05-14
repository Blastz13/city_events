import pytest

from httpx import AsyncClient
from app.server import app
from app.user.services import UserService
from core.db.session import Base, sync_engine


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
async def client_auth(init_user):
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        client.headers["Authorization"] = f'Bearer {init_user[1].token}'
        yield client


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


@pytest.fixture(scope="session", autouse=True)
async def init_user():
    user = await UserService().create_user(email="test@mail.ru", password1="pass", password2="pass", username="test")
    credentials = await UserService().login(email="test@mail.ru", password="pass")
    return user, credentials


@pytest.fixture()
def create_event_data():
    return {
        "title": "string",
        "description": "string",
        "link": "string",
        "date_start": "2023-05-13T23:25:52.208+00:00",
        "limit_member": 0,
        "location": "string",
        "longitude": 0,
        "latitude": 0
    }
