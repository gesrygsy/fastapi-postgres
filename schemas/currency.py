from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class CurrnBase(BaseModel):
    # function: str
    symbol: str
    datetime: datetime
    open: float
    high: float
    low: float
    close: float

    volume: Optional[float] = None


class CurrnCreate(CurrnBase):
    ...


class CurrnShow(CurrnBase):
    dataset_function: str


class Currn(CurrnBase):
    id: int
    dataset_function: str

    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True