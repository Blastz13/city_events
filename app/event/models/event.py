from sqlalchemy import Column, BigInteger, Boolean, Integer, func, String, Float, select, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import session

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
    comments = relationship("Comment", backref="event")


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


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), index=True, nullable=False)
    comment = Column(String, nullable=False)
    rating = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)


class AchievementUsers(Base):
    __tablename__ = "achievement_users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


#
# class City(Base):
#     """A city, including its geospatial data."""
#
#     __tablename__ = "cities"
#
#     point_id = Column(Integer, primary_key=True, autoincrement=True)
#     location = Column(String(30))
#     longitude = Column(Float)
#     latitude = Column(Float)
#     geo = Column(Geometry(geometry_type="POINT"))
#
#     def __repr__(self):
#         return "<City {name} ({lat}, {lon})>".format(
#             name=self.location, lat=self.latitude, lon=self.longitude)
#
#     async def get_cities_within_radius(self, radius):
#         """Return all cities within a given radius (in meters) of this city."""
#
#         return await session.execute(select(City).where(func.ST_DistanceSphere(City.geo, self.geo) == radius))
#
#     @classmethod
#     async def add_city(cls, location, longitude, latitude):
#         """Put a new city in the database."""
#
#         geo = 'POINT({} {})'.format(longitude, latitude)
#         city = City(location=location,
#                     longitude=longitude,
#                     latitude=latitude,
#                     geo=geo)
#         session.add(city)
#         await session.commit()
#
#     @classmethod
#     def update_geometries(cls):
#         """Using each city's longitude and latitude, add geometry data to db."""
#
#         cities = City.query.all()
#
#         for city in cities:
#             point = 'POINT({} {})'.format(city.longitude, city.latitude)
#             city.geo = point
#
#         session.commit()
