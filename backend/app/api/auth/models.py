from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr
    full_name: str | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str | None = None
    disabled: bool | None = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    disabled: bool | None = False


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    user_id: int