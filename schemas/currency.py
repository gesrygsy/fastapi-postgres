from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class CurrnBase(BaseModel):
    symbol: str
    datetime: datetime
    open: float
    high: float
    low: float
    close: float

    volume: Optional[float] = None


class CurrnCreate(CurrnBase):
    ...


class Currn(CurrnBase):
    id: int
    dataset_function: str = "FX"

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True