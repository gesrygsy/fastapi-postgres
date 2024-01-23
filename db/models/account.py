from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..database import Base
from .user import User
from .mixins import Timestamp


class Accounts(Timestamp, Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    account = Column(String(50), nullable=False)
    server = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_name = Column(String(50), ForeignKey("users.username"), nullable=False)
    owner_email = Column(String(100), ForeignKey("users.email"), nullable=False)

    user_id = relationship("User", foreign_keys=[owner_id])
    username = relationship("User", foreign_keys=[owner_name])
    email = relationship("User", foreign_keys=[owner_email])

    last_access = Column(DateTime, default=datetime.utcnow, nullable=False)
