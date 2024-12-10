from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLogMiddleware,
    SQLAlchemyMiddleware,
)
from core.helpers.cache import Cache, CustomKeyMaker, RedisBackend

# from core.openfund.openfund import openfund as op
from core.openfund.scheduler import scheduler
from core.openfund.base_tool import Pool

from app.container import Container
from app.auth.adapter.input.api import router as auth_router
from app.user.adapter.input.api import router as user_router
from app.openfund.adapter.input.api import router as collect_router


def init_routers(app_: FastAPI) -> None:
    container = Container()
    user_router.container = container
    auth_router.container = container
    collect_router.container = container
    app_.include_router(user_router)
    app_.include_router(auth_router)
    app_.include_router(collect_router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

def init_tools_pool() -> None:
    Pool.init()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在异步上下文管理器中，"进入上下文"时启动
    # logger.debug(f"+++++++++++ lifespan startting... +++++++++++")
    # Openfund()
    scheduler.start()
    # yield
    yield
    # 在异步上下文管理器中，"退出上下文"时释放资源
    scheduler.shutdown()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Openfund",
        description="Openfund API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
        lifespan=lifespan,
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    init_tools_pool()
    return app_


app = create_app()
