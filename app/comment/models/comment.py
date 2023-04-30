from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), index=True, nullable=False)
    comment = Column(String, nullable=False)
    rating = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)

    user = relationship('User', backref='comments', lazy='joined')
    event = relationship('Event', back_populates='comments', lazy='joined')
