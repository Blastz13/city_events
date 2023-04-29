from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from core.db.mixins import TimestampMixin
from db import Base


class ChatRoom(Base, TimestampMixin):
    __tablename__ = 'chat_room'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('queue.id'))
    event = relationship("Event", backref=backref("chat", uselist=False))
