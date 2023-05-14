import pytest

from app.achievement.services import AchievementService
from app.user.services import UserService
from core.exceptions import NotFoundException
from tests.factories import AchievementModelFactory


@pytest.mark.asyncio
async def test_get_achievement_list(client_auth):
    AchievementModelFactory.create_batch(10)
    response = await client_auth.get(f"/api/v1/achievement")
    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.asyncio
async def test_assign_achievement(client_auth):
    achievement = AchievementModelFactory()
    response = await client_auth.post(f"/api/v1/achievement/{achievement.id}", json={"user_id": 1})
    assert response.status_code == 201
    user = await UserService().get_user_or_404(1)
    assert user.achievements is not None


@pytest.mark.asyncio
async def test_delete_achievement(client_auth):
    achievement = AchievementModelFactory()
    response = await client_auth.delete(f"/api/v1/achievement/{achievement.id}")
    assert response.status_code == 204
    with pytest.raises(NotFoundException):
        await AchievementService().get_achievement_or_404(achievement.id)
