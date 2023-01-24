from typing import Any
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from ..common.models import ResponseModel


class UserBase(SQLModel):
    email: EmailStr = Field(default='seyi@gmail.com')
    full_name: str | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str | None = None
    disabled: bool | None = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int = Field(default=2)
    disabled: bool | None = False


class Token(SQLModel):
    access_token: str = Field(
        default=
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMCIsImV4cCI6MTY3NDU4NTE3Nn0.jCEcE16vanjOc_rwp_JG5UdvBXj9F2j2tiZ286B3Fes'
    )
    token_type: str = Field(default='bearer')


class TokenData(SQLModel):
    user_id: int
