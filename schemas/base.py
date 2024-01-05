from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    function: str
    type: int = 1

    description: Optional[str] = None
    data_source: Optional[str] = None


class DatasetCreate(Base):
    ...


class Dataset(Base):
    # id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True