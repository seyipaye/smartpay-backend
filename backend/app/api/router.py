from fastapi.routing import APIRouter

from .auth.views import router as auth_router
from .transactions.views import router as transactions_router
from .common.views import router as common_router

# from ..v1.communication.views import router as communication_router

# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi import Depends, FastAPI, HTTPException, status
# # from sqlalchemy.orm import Session

# from ..v1.auth.views import login
# from ..v1 import deps
# from ..v1.auth.schemas import UserLogin

api_router_v1 = APIRouter()

# @api_router_v1.post("/docs/token", include_in_schema=False)
# async def token(form_data: OAuth2PasswordRequestForm = Depends(),
#                 db: Session = Depends(deps.get_db)):
#     """
#     The an endpoint for quick login from the documentation

#     Returns:
#         UserOut: return a UserOut schema with a token object.
#     """

#     val = await login(UserLogin(username=form_data.username), db=db)

#     access_token = val['data']['access_token']

#     return {"access_token": access_token['token'], "token_type": "bearer"}

api_router_v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router_v1.include_router(
    transactions_router,
    prefix="/transactions",
    tags=["Transactions"],
)
api_router_v1.include_router(common_router, prefix="/common", tags=["Common"])
