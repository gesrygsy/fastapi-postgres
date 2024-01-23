# import enum
from strenum import StrEnum

from sqlalchemy import Column, String, Enum, Text
from sqlalchemy.orm import relationship

from ..database import Base
from .mixins import Timestamp


# class SymbolType(enum.IntEnum):
#     currency = 1
#     commodity = 2
#     etf = 3
#     stock = 4
#     bond = 5
#     crypto = 6


class SymbolType(StrEnum):
    currency = "Currency"
    commodity = "Commodity"
    etf = "ETF"
    stock = "Stock"
    bond = "Bond"
    crypto = "Crypto"

    # @classmethod
    # def _missing_(cls, value):
    #     value = value.lower()
    #     for member in cls:
    #         if member == value:
    #             return member
    #     return None


class Dataset(Timestamp, Base):
    __tablename__ = "dataset"

    function = Column(String(100), primary_key=True, nullable=False)
    type = Column(Enum(SymbolType), nullable=False)
    # type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    data_source = Column(String(100), nullable=True)

    currency = relationship("Currn", back_populates="dataset")