from typing import Optional
from pydantic import BaseModel, SecretStr


class Login(BaseModel):
    username: str
    password: SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None