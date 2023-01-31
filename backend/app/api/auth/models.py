from typing import Any
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
import uuid as uuid_pkg

from ..common.models import ResponseModel


class UserBase(SQLModel):
    email: EmailStr = Field(default='seyi@gmail.com')
    full_name: str | None = None


class User(UserBase, table=True):
    # id: int = Field(default=None, primary_key=True)
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    hashed_password: str | None = None
    disabled: bool | None = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str = Field(default='e3528ffa-d4a3-4133-b991-c230ae0dfbbf')
    disabled: bool | None = False


class LoginRequest(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str = Field(
        default=
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMCIsImV4cCI6MTY3NDU4NTE3Nn0.jCEcE16vanjOc_rwp_JG5UdvBXj9F2j2tiZ286B3Fes'
    )
    token_type: str = Field(default='bearer')


class TokenData(SQLModel):
    user_id: str
