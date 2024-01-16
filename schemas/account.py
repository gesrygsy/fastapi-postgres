from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    account: int | str
    server: str
    password: str


class AccountCreate(Base):
    ...


class Account(Base):
    id: int
    created_at: datetime
    updated_at: datetime
    last_access: datetime

    class Config:
        from_attributes = True


class ShowAccount(Account):
    account: int | str
    server: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    last_access: datetime
