from sqlalchemy import Column, BigInteger, Boolean, Integer, String

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    rating = Column(Integer, default=0, nullable=False)
