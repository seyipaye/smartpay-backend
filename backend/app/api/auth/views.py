from datetime import timedelta
from sqlmodel import Session

from ..utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .models import UserCreate, User, UserRead, LoginRequest, Token  #ResponseSchema, ResponseModel

from ..common.models import ResponseModel

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from core.engine import get_db
from ..utils import jwt_util

from ..utils.crypt_util import (
    get_password_hash,
    verify_password,
)

from .crud import (
    create_user,
    get_user,
)

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/signup",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK:
        ResponseModel.example(
            description='Signup Successful',
            data={
                'user': UserRead().dict(),
                'token': Token().dict()
            },
        ),
    },
)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    fetched_user = get_user(user.email, db)
    if fetched_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        # Create a new user
        db_user = User.from_orm(user)
        db_user.hashed_password = get_password_hash(user.password)
        await create_user(db_user, db)

    except Exception as ex:
        print(ex.args)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token to authorize user to access further endpoints
    access_token = create_access_token(db_user.id)

    return ResponseModel.success(
        message='Signup successful',
        data={
            'user': db_user,
            'token': access_token,
        },
    )


@router.post(
    "/login",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK:
        ResponseModel.example(
            description='Login Successful',
            data={
                'user': UserRead().dict(),
                'token': Token().dict()
            },
        ),
    },
)
async def login(
        request: LoginRequest,
        db: Session = Depends(get_db),
):
    user = authenticate_user(request.email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)
    return ResponseModel.success(
        message='Login successful',
        data={
            'user': user,
            'token': token,
        },
    )


@router.post(
    "/token",
    include_in_schema=False,
    response_model=Token,
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_access_token(user.id)


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(id):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt_util.create_access_token(
        data={"sub": str(id)},
        expires_delta=access_token_expires,
    )
