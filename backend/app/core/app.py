from api.router import api_router_v1
from fastapi import FastAPI
from .engine import create_db_and_tables
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from collections import defaultdict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.common.models import ResponseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup():
        create_db_and_tables()

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await database.disconnect()

    #create and mount version 1 of soberpal API
    appv1 = FastAPI(
        title="Swift Pay Project",
        description="Swift Pay API",
        docs_url="/docs",
        version="1.0",
        redoc_url="/redoc",
        openapi_url="/open.json",
        default_response_class=UJSONResponse,
        responses={
            status.HTTP_400_BAD_REQUEST:
            ResponseModel.example(
                status=False,
                description='Validation error: Invalid request',
                message=
                'Error: Title field required, Error: Image field required',
                data={
                    "title": ["field required"],
                    "image": ["field required"]
                },
            ),
        },
    )

    @appv1.exception_handler(RequestValidationError)
    async def validation_error_handler(request, exc):
        reformatted_message = defaultdict(list)
        human_friendly_message = ''

        for pydantic_error in exc.errors():
            loc, msg = pydantic_error["loc"], pydantic_error["msg"]
            filtered_loc = loc[1:] if loc[0] in ("body", "query",
                                                 "path") else loc
            field_string = ",".join(
                filtered_loc)  # nested fields with dot-notation
            reformatted_message[field_string].append(msg)

            human_friendly_message += f'Error: {field_string.title()} {msg}, '

        # Remove trailing comma
        human_friendly_message = human_friendly_message.rstrip(', ')

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseModel.error(
                message=human_friendly_message,
                data=reformatted_message,
            ),
        )

    @appv1.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):

        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel.error(
                message=str(exc.detail),
                data=None,
            ),
        )

    appv1.include_router(router=api_router_v1)
    app.mount("/api/v1", appv1)

    # #create and mount version 2 of soberpal API
    # appv2 = FastAPI(title="Soberpal Project V2",
    #                 description="Soberpal API V2",
    #                 version="2.0",
    #                 docs_url="/docs/",
    #                 redoc_url="/redoc/",
    #                 openapi_url="/open.json",
    #                 default_response_class=UJSONResponse
    #             )

    # appv2.include_router(router=api_router_v2)
    # app.mount("/api/v2", appv2)

    return app
