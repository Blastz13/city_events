import datetime

import pytest

from core.db.session import session
from core.exceptions import NotFoundException
from tests.factories import EventModelFactory

from app.event.models import EventOrganizators
from app.event.services import EventService


@pytest.mark.asyncio
async def test_create_no_auth_event(client, create_event_data):
    response = await client.post("/api/v1/events", json=create_event_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_auth_event(client_auth, create_event_data):
    response = await client_auth.post("/api/v1/events", json=create_event_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_upcoming_event(client_auth):
    data = {
        "title": "string",
        "description": "string",
        "link": "string",
        "date_start": datetime.datetime.now() + datetime.timedelta(minutes=30),
        "limit_member": 0,
        "location": "string",
        "longitude": 0,
        "latitude": 0
    }
    await EventService().create_event(user_id=1, **data)
    response = await client_auth.get("/api/v1/events/upcoming")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_add_no_auth_member_to_event(client):
    event = EventModelFactory()
    response = await client.post(f"/api/v1/events/{event.id}/invite")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_auth_member_to_event(client_auth):
    event = EventModelFactory()
    response = await client_auth.post(f"/api/v1/events/{event.id}/invite")
    assert response.status_code == 201
    event = await EventService().get_event_or_404(event.id)
    assert event.members is not None


@pytest.mark.asyncio
async def test_add_auth_member_to_event_limit(client_auth):
    event = EventModelFactory(limit_member=0)
    response = await client_auth.post(f"/api/v1/events/{event.id}/invite")
    assert response.status_code == 400
    event = await EventService().get_event_or_404(event.id)
    assert len(event.members) == 0


@pytest.mark.asyncio
async def test_delete_event(client_auth, init_user):
    event = EventModelFactory()
    session.add(EventOrganizators(user_id=init_user[0].id, event_id=event.id))
    await session.commit()

    response = await client_auth.delete(f"/api/v1/events/{event.id}")
    assert response.status_code == 204
    with pytest.raises(NotFoundException):
        await EventService().get_event_or_404(event.id)


@pytest.mark.asyncio
async def test_delete_event_forbidden_user(client_auth, init_user):
    event = EventModelFactory()
    response = await client_auth.delete(f"/api/v1/events/{event.id}")
    assert response.status_code == 403
