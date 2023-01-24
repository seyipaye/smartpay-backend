from datetime import timedelta
from sqlmodel import Session

from ..utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .models import UserCreate, User, UserRead, Token  #ResponseSchema, ResponseModel

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
    # login_user,
    create_user,
    get_user,
)
from fastapi.security import OAuth2PasswordRequestForm
# from deps import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):

    # Check if the user exists
    fetched_user = get_user(user.email, db)
    if fetched_user:
        return {"status_code": 400, "message": "User already signed up!"}

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

    # user_out = schemas.UserOut(**db_user.__dict__, access_token=access_token)
    # "user": UserObjectSchema(**jsonable_encoder(user)),
    # "token": access_token,
    # Serialize user object.
    # results = {
    #     "user": UserObjectSchema(**jsonable_encoder(user)),
    #     "token": access_token,
    #     "status_code": 201,
    #     "message": "Welcome! Proceed to the login page...",
    # }
    return {'user': db_user, 'token': access_token}


@router.post(
    "/login",
    # response_model=AuthResponse,
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
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    return await login_for_access_token(form_data=form_data, db=db)


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
