from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    username: str
    email: str
    password: str
    role: int = 2


class UserCreate(Base):
    ...


class User(Base):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    id: int
    is_active: bool
    username: str
    email: str

    class Config:
        from_attributes = True