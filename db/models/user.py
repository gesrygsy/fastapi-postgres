import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum

from ..database import Base
from .mixins import Timestamp


class Role(enum.IntEnum):
    admin = 1
    user = 2


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(Role))
    is_active = Column(Boolean, default=True)
    