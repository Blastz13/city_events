import datetime

import pytest

from httpx import AsyncClient

from app.achievement.models import Achievement
from app.event.models import Event
from app.server import app
from app.user.services import UserService
from core.db.elastic_db import init_elastic
from core.db.session import Base, sync_engine, sync_session
from tests.factories import EventModelFactory, AchievementModelFactory


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
async def init_elasticsearch():
    await init_elastic()


@pytest.fixture(scope="session", autouse=True)
async def init_user():
    user = await UserService().create_user(email="test@mail.ru", password1="pass",
                                           password2="pass", username="test", is_admin=True)
    credentials = await UserService().login(email="test@mail.ru", password="pass")
    return user, credentials


@pytest.fixture(scope="session")
def list_achievements():
    achievements = AchievementModelFactory.create_batch(10)
    yield achievements
    sync_session.query(Achievement).filter(
        Achievement.id.in_([achievement.id for achievement in achievements])
    ).delete(synchronize_session='fetch')
    sync_session.commit()

@pytest.fixture(scope="session")
def list_events():
    events = EventModelFactory.create_batch(10)
    yield events
    sync_session.query(Event).filter(Event.id.in_([event.id for event in events])).delete(synchronize_session='fetch')
    sync_session.commit()


@pytest.fixture(scope="session")
def achievement():
    achievement = AchievementModelFactory()
    yield achievement
    sync_session.delete(achievement)
    sync_session.commit()


@pytest.fixture(scope="session")
def event():
    event = EventModelFactory()
    yield event
    sync_session.delete(event)
    sync_session.commit()


@pytest.fixture()
def create_event_data():
    return {
        "title": "string",
        "description": "string",
        "link": "string",
        "date_start": datetime.datetime.now(),
        "limit_member": 0,
        "location": "string",
        "longitude": 0,
        "latitude": 0
    }
