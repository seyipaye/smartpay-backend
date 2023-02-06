from datetime import datetime
from typing import Any, List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
import uuid as uuid_pkg

from ..common.models import ResponseModel


class UserBase(SQLModel):
    email: EmailStr = Field(default='seyi@gmail.com')
    username: str | None = None


class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    hashed_password: str | None = None
    disabled: bool | None = False
    wallet: "Wallet" = Relationship(sa_relationship_kwargs={
        'uselist': False,
    }, )


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str = Field(default='e3528ffa-d4a3-4133-b991-c230ae0dfbbf')
    disabled: bool | None = False


class Wallet(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    balance: int = Field(default=0)
    active: bool = Field(default=True)
    updated_at: datetime = Field(default=datetime.utcnow())
    user_id: None | uuid_pkg.UUID = Field(
        default=None,
        foreign_key="user.id",
    )


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
