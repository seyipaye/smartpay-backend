from sqlmodel import Session
from ..auth.models import User

# from .models import Event  #ResponseSchema, ResponseModel

from ..common.models import ResponseModel

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from core.engine import get_db

from .crud import (
    update_wallet,
    get_wallet,
)

from ..utils.jwt_util import get_current_user

router = APIRouter()

# logger = logging.getLogger(__name__)

# raise HTTPException(
#     status_code=status.HTTP_400_BAD_REQUEST,
#     detail="Email already exists",
#     headers={"WWW-Authenticate": "Bearer"},
# )


@router.post(
    "/pay/{wallet_id}",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK:
        ResponseModel.example(
            description='Payemnt Successful',
            data={
                'user': 'UserRead().dict()',
                'token': 'Token().dict()'
            },
        ),
    },
)
async def pay(
    wallet_id: str,
    amount: int,
    db=Depends(get_db),
    user: User = Depends(get_current_user)
) -> dict:

    # Check if wallet is not the user wallet
    # Check if balance is sufficient
    # Check if wallet_id is valid
    # Subtract money from from_wallet, and add to to_wallet
    # Send notification to parties
    # return a success response

    # Mobile app should fetch latest balance from db

    # Check if balance is sufficient
    from_wallet = user.wallet
    if from_wallet.balance <= amount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insufficient balance for transaction",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if wallet_id is valid
    to_wallet = get_wallet(wallet_id, db)
    if to_wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet Id is not valid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Subtract money from curent wallet, and add to the other wallet
    from_wallet.balance -= amount
    to_wallet.balance += amount
    update_wallet(from_wallet, db)
    update_wallet(to_wallet, db)

    # Send notification to parties
    # return a success response

    # print(user)
    # session.add(new_event)
    # session.commit()
    # session.refresh(new_event)

    return ResponseModel.success(
        message='Transaction Successful',
        data=to_wallet,
    )


@router.post(
    "/top-up",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK:
        ResponseModel.example(
            description='Payemnt Successful',
            data={
                'user': 'UserRead().dict()',
                'token': 'Token().dict()'
            },
        ),
    },
)
async def top_up(
    amount: int, db=Depends(get_db), user: User = Depends(get_current_user)
) -> dict:

    to_wallet = user.wallet

    # Subtract money from curent wallet, and add to the other wallet
    to_wallet.balance += amount
    update_wallet(to_wallet, db)

    # Send notification to parties
    # return a success response

    # print(user)
    # session.add(new_event)
    # session.commit()
    # session.refresh(new_event)

    return ResponseModel.success(
        message='Top-Up Successful',
        data=to_wallet,
    )


@router.get(
    "/wallet",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK:
        ResponseModel.example(
            description='Payemnt Successful',
            data={
                'user': 'UserRead().dict()',
                'token': 'Token().dict()'
            },
        ),
    },
)
async def wallet(
        db=Depends(get_db),
        user: User = Depends(get_current_user),
) -> dict:

    # balance = user.wallet.balance

    # Send notification to parties
    # return a success response

    # print(user)
    # session.add(new_event)
    # session.commit()
    # session.refresh(new_event)

    return ResponseModel.success(
        message='Successful',
        data=user.wallet,
    )


# @router.post(
#     "/login",
#     response_model=ResponseModel,
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_200_OK:
#         ResponseModel.example(
#             description='Login Successful',
#             data={
#                 'user': UserRead().dict(),
#                 'token': Token().dict()
#             },
#         ),
#     },
# )
# async def login(
#         request: LoginRequest,
#         db: Session = Depends(get_db),
# ):
#     user = authenticate_user(request.email, request.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     token = create_access_token(user.id)
#     return ResponseModel.success(
#         message='Login successful',
#         data={
#             'user': user,
#             'token': token,
#         },
#     )

# @router.post(
#     "/token",
#     include_in_schema=False,
#     response_model=Token,
# )
# async def login_for_access_token(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return create_access_token(user.id)

# def authenticate_user(email: str, password: str, db: Session):
#     user = get_user(email, db)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(id):
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     return jwt_util.create_access_token(
#         data={"sub": str(id)},
#         expires_delta=access_token_expires,
#     )
