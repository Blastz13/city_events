import factory

from app.achievement.models import Achievement
from app.event.models import Event
from core.db.session import sync_session
from pytest_factoryboy import register


@register
class AchievementModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Achievement
        sqlalchemy_session = sync_session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker("name")
    image_url = factory.Faker("name")


@register
class EventModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = sync_session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker("name")
    description = factory.Faker("text")
    limit_member = factory.Faker("random_int")
    location = factory.Faker("address")
    longitude = factory.Faker("longitude")
    latitude = factory.Faker("longitude")
    geo = 'POINT(1.1 1.1)'
