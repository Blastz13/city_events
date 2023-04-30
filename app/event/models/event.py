from sqlalchemy import Column, BigInteger, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin
from geoalchemy2 import Geometry


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, db_index=True)
    description = Column(String(255), nullable=False)
    link = Column(String(255))
    date_start = Column(DateTime)
    rating = Column(Integer, default=0, nullable=False)
    limit_member = Column(Integer, default=0, nullable=False)
    location = Column(String(127), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    geo = Column(Geometry(geometry_type="POINT"), nullable=False)

    organizators = relationship('User', secondary='event_organizators', backref='event_organizators', lazy='joined')
    members = relationship('User', secondary='event_members', backref='event_members', lazy='joined')
    comments = relationship("Comment", back_populates="event", lazy='joined')


class EventMembers(Base):
    __tablename__ = "event_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))


class EventOrganizators(Base):
    __tablename__ = "event_organizators"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))


class AchievementUsers(Base):
    __tablename__ = "achievement_users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
