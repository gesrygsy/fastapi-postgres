from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from ..database import Base
from .base import Dataset
from .mixins import Timestamp


class Currn(Timestamp, Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)

    volume = Column(Float, nullable=True)

    dataset_function = Column(String(50), ForeignKey("dataset.function"), nullable=False)

    dataset = relationship(Dataset, back_populates="currency")
