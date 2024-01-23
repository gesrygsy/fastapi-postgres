from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    function: str
    type: str

    description: Optional[str] = None
    data_source: Optional[str] = None


class DatasetCreate(Base):
    ...


class DatasetUpdate(BaseModel):
    type: str

    description: Optional[str] = None
    data_source: Optional[str] = None
    updated_at: datetime


class Dataset(Base):
    # id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True