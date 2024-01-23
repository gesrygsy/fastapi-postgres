from datetime import datetime
import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime#, ForeignKey
# from sqlalchemy.orm import relationship

from ..database import Base
# from .accounts import Accounts
from .mixins import Timestamp


class Role(enum.IntEnum):
    admin = 1
    user = 2


# RoleStatus: Enum = Enum(
#     Role,
#     name="symbol_type_status",
#     create_constraint=True,
#     metadata=Base.metadata,
#     validate_strings=True,
# )


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(Role), nullable=False)
    is_active = Column(Boolean, default=False)
    token = Column(String(200), nullable=True)

    last_access = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # account_id = Column(Integer, ForeignKey("accounts.id"))

    # accounts = relationship("Accounts", back_populates="users")
