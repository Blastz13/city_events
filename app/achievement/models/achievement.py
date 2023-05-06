from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    users = relationship('User', secondary='achievement_users', back_populates='achievements', lazy='joined')
    image_url = Column(String)


class AchievementUsers(Base):
    __tablename__ = "achievement_users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
