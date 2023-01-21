from api.router import api_router_v1
from fastapi import FastAPI
from .engine import create_db_and_tables
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware


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
