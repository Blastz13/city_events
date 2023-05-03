import asyncio
import logging

from sqlalchemy import Column, BigInteger, Integer, String, Float, ForeignKey, TIMESTAMP, event
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin
from geoalchemy2 import Geometry
from app.comment.models import Comment
from core.db.elastic_db import es_client, ELASTICSEARCH_INDEX

logger = logging.getLogger('app')


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, db_index=True)
    description = Column(String(255), nullable=False)
    link = Column(String(255))
    date_start = Column(TIMESTAMP(timezone=True))
    rating = Column(Integer, default=0, nullable=False)
    limit_member = Column(Integer, default=0, nullable=False)
    location = Column(String(127), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    geo = Column(Geometry(geometry_type="POINT"), nullable=False)

    organizators = relationship('User', secondary='event_organizators', backref='event_organizators', lazy='joined')
    members = relationship('User', secondary='event_members', backref='event_members', lazy='joined')
    comments = relationship(Comment, back_populates="event", lazy='joined')


@event.listens_for(Event, "after_insert")
def index_document(_, __, target):
    logger.info(f"triggered event.after_insert update {target.id} in elastic")
    doc = {
        "title": target.title,
        "description": target.description
    }
    loop = asyncio.get_event_loop()
    loop.create_task(es_client.index(index=ELASTICSEARCH_INDEX, id=target.id, body=doc))


@event.listens_for(Event, "after_insert")
def index_document(_, __, target):
    logger.info(f"triggered event.after_insert update {target.id} in elastic")
    doc_update = {
        "doc": {
            "title": target.title,
            "description": target.description
        }
    }
    loop = asyncio.get_event_loop()
    loop.create_task(es_client.update(index=ELASTICSEARCH_INDEX, id=target.id, body=doc_update))


@event.listens_for(Event, "after_delete")
def index_document(_, __, target):
    logger.info(f"triggered event.after_delete update {target.id} in elastic")
    loop = asyncio.get_event_loop()
    loop.create_task(es_client.delete(index=ELASTICSEARCH_INDEX, id=target.id))


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
