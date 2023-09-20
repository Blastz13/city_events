import pytest

from app.event.models import Event
from core.exceptions import NotFoundException
from app.event.services import EventService
from pytest_lazyfixture import lazy_fixture

import sqlalchemy


@pytest.mark.asyncio
@pytest.mark.parametrize("skip, limit, expected", [
    (0, 10, 10),
    (0, 5, 5),
    (0, 0, 0),
    pytest.param(-10, -1, 0, marks=pytest.mark.xfail(raises=sqlalchemy.exc.DBAPIError)),
])
async def test_get_event_list(list_events, skip, limit, expected):
    events = await EventService().get_event_list(skip=skip, limit=limit)
    assert len(events) == expected


@pytest.mark.parametrize("_id, _event", [
    (1, lazy_fixture('event')),
    pytest.param(101, lazy_fixture('event'), marks=pytest.mark.xfail(raises=NotFoundException)),
])
@pytest.mark.asyncio
async def test_add_members_to_event(_id, _event):
    _event = await EventService().add_members_to_event(user_id=_id, event_id=_event.id)
    assert _event


@pytest.mark.asyncio
@pytest.mark.parametrize("_event, expected", [
    (lazy_fixture('event'), 10),
    ('404', 10),
])
async def test_get_events_by_query(expected, _event):
    title = _event.title if isinstance(_event, Event) else _event

    events = await EventService().get_events_by_query(
        query=title,
        date_start=None,
        date_end=None,
        offset=0,
        limit=10
    )
    assert len(events) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("_id", [
    1,
    pytest.param(101, marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_get_event_or_404(_id):
    _event = await EventService().get_event_or_404(id=_id)
    assert _event


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, event_data", [
    (1, lazy_fixture('create_event_data')),
    pytest.param(111, lazy_fixture('create_event_data'), marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_create_event(user_id, event_data):
    event = await EventService().create_event(user_id=user_id, **event_data)
    assert event


@pytest.mark.asyncio
@pytest.mark.parametrize('radius, excepted', [
    (0, 0),
    (1, 1),
])
async def test_get_events_by_radius(event, radius, excepted):
    _event = await EventService().get_events_by_radius(radius=radius, longitude=event.longitude,
                                                       latitude=event.latitude)
    assert len(_event) == excepted


@pytest.mark.asyncio
async def test_get_upcoming_events(event):
    _event = await EventService().get_upcoming_events()
    assert _event


@pytest.mark.asyncio
@pytest.mark.parametrize("_event", [
    (lazy_fixture('event')),
    pytest.param(101, marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_remove_event(_event):
    _id = _event.id if isinstance(_event, Event) else _event
    _event = await EventService().remove_event(id=_id)
    assert _event == {}
