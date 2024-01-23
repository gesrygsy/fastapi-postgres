from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class Base(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    

class UserCreate(Base):
    ...


class User(Base):
    id: int
    is_active: bool
    token: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    token: str
    role: int

    class ConfigDict:
        from_attributes = True


class UserToken(BaseModel):
    token: str