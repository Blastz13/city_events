import pytest

from app.achievement.models import Achievement
from app.achievement.services import AchievementService
from core.exceptions import NotFoundException
from pytest_lazyfixture import lazy_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize("_achievement", [
    (lazy_fixture('achievement')),
    pytest.param(101, marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_get_achievement_or_404(_achievement):
    _id = _achievement.id if isinstance(_achievement, Achievement) else _achievement
    _achievement = await AchievementService().get_achievement_or_404(id=_id)
    assert _achievement


@pytest.mark.asyncio
async def test_get_achievement_list(list_achievements):
    achievements = await AchievementService().get_achievement_list(limit=10)
    assert len(achievements) == len(list_achievements)


@pytest.mark.asyncio
@pytest.mark.parametrize("_achievement, user_id", [
    (lazy_fixture('achievement'), 1),
    pytest.param(lazy_fixture('achievement'), 101, marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_assign_achievement(_achievement, user_id):
    _achievement = await AchievementService().assign_achievement(achievement_id=_achievement.id, user_id=user_id)
    assert _achievement


@pytest.mark.asyncio
@pytest.mark.parametrize("title, expected", [
    ('', ''),
    ('1@!#312', '1@!#312'),
    ('ABC', 'ABC')
])
async def test_update_achievement(achievement, title, expected):
    payload = {
        'title': title
    }
    _achievement = await AchievementService().update_achievement(id=achievement.id, file=None, **payload)
    assert _achievement.title == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("_achievement", [
    (lazy_fixture('achievement')),
    pytest.param(101, marks=pytest.mark.xfail(raises=NotFoundException))
])
async def test_remove_achievement(_achievement):
    _id = _achievement.id if isinstance(_achievement, Achievement) else _achievement
    achievement = await AchievementService().remove_achievement(id=_id)
    assert achievement == {}