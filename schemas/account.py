from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    name: str
    account: int | str
    server: str
    password: str

    owner_id: int
    owner_name: str
    owner_email: str


class AccountCreate(BaseModel):
    name: str
    account: str
    server: str
    password: str

    owner_name: str


class AccountUpdate(BaseModel):
    name: str
    account: str
    server: str
    owner_name: str

    new_name: str
    new_account: str
    new_server: str
    new_password: str


class Account(Base):
    id: int
    created_at: datetime
    updated_at: datetime
    last_access: datetime

    class ConfigDict:
        from_attributes = True


class ShowAccount(BaseModel):
    name: str
    account: int | str
    server: str
    owner_name: str
    owner_email: str
    created_at: datetime
    updated_at: datetime
    last_access: datetime

    class ConfigDict:
        from_attributes = True


# class AccountDelete(BaseModel):
#     name: str
#     account: str
#     server: str

#     owner_name: str