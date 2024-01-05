import enum

from sqlalchemy import Column, String, Enum, Text
from sqlalchemy.orm import relationship

from ..database import Base
from .mixins import Timestamp


class SymbolType(enum.IntEnum):
    currency = 1
    etf = 2
    stock = 3
    bond = 4
    crypto = 5


class Dataset(Timestamp, Base):
    __tablename__ = "dataset"

    function = Column(String(100), primary_key=True, nullable=False)
    type = Column(Enum(SymbolType), nullable=False)
    description = Column(Text, nullable=True)
    data_source = Column(String(100), nullable=True)

    currency = relationship("Currn", back_populates="dataset")