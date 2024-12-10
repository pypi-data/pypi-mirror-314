# arpakit

from __future__ import annotations

import asyncio
import logging
import os.path
import pathlib
import threading
import traceback
from datetime import datetime
from typing import Any, Callable

import fastapi.exceptions
import fastapi.responses
import starlette.exceptions
import starlette.requests
import starlette.status
from fastapi import FastAPI, APIRouter, Query
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from jaraco.context import suppress
from pydantic import BaseModel, ConfigDict
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_to_json_str_to_json_obj
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_operation_execution_util import ExecuteOperationWorker
from arpakitlib.ar_sqlalchemy_model_util import StoryLogDBM
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB
from arpakitlib.ar_type_util import raise_for_type, raise_if_not_async_func

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if not (
                cls.__name__.endswith("SO")
                or cls.__name__.endswith("SI")
                or cls.__name__.endswith("SchemaIn")
                or cls.__name__.endswith("SchemaOut")
        ):
            raise ValueError("APISchema class should ends with SO | SI | SchemaIn | SchemaOut")
        super().__init_subclass__(**kwargs)


class BaseSI(BaseSchema):
    pass


class BaseSO(BaseSchema):
    pass


class SimpleSO(BaseSO):
    id: int
    long_id: str
    creation_dt: datetime


class ErrorSO(BaseSO):
    class APIErrorCodes(Enumeration):
        cannot_authorize = "CANNOT_AUTHORIZE"
        unknown_error = "UNKNOWN_ERROR"
        error_in_request = "ERROR_IN_REQUEST"
        not_found = "NOT_FOUND"

    has_error: bool = True
    error_code: str | None = None
    error_code_specification: str | None = None
    error_description: str | None = None
    error_data: dict[str, Any] = {}


class RawDataSO(BaseSO):
    data: dict[str, Any] = {}


class StoryLogSO(SimpleSO):
    level: str
    title: str | None
    data: dict[str, Any]


class OperationSO(SimpleSO):
    execution_start_dt: datetime | None
    execution_finish_dt: datetime | None
    status: str
    type: str
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: dict[str, Any]
    duration_total_seconds: float | None


class APIJSONResponse(fastapi.responses.JSONResponse):
    def __init__(self, *, content: BaseSO, status_code: int = starlette.status.HTTP_200_OK):
        self.content_ = content
        self.status_code_ = status_code
        super().__init__(
            content=safely_transfer_to_json_str_to_json_obj(content.model_dump()),
            status_code=status_code
        )


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = starlette.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = ErrorSO.APIErrorCodes.unknown_error,
            error_code_specification: str | None = None,
            error_description: str | None = None,
            error_data: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_code_specification = error_code_specification
        self.error_description = error_description
        if error_data is None:
            error_data = {}
        self.error_data = error_data

        self.error_so = ErrorSO(
            has_error=True,
            error_code=self.error_code,
            error_specification=self.error_code_specification,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.error_so.model_dump(mode="json")
        )


def create_handle_exception(
        *,
        funcs_before_response: list[Callable] | None = None,
        async_funcs_after_response: list[Callable] | None = None,
) -> Any:
    if funcs_before_response is None:
        funcs_before_response = []

    if async_funcs_after_response is None:
        async_funcs_after_response = []

    async def handle_exception(
            request: starlette.requests.Request, exception: Exception
    ) -> APIJSONResponse:
        status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR

        error_so = ErrorSO(
            has_error=True,
            error_code=ErrorSO.APIErrorCodes.unknown_error,
            error_data={
                "exception_type": str(type(exception)),
                "exception_str": str(exception),
                "request.method": str(request.method),
                "request.url": str(request.url),
            }
        )

        if isinstance(exception, APIException):
            old_error_data = error_so.error_data
            error_so = exception.error_so
            error_so.error_data = combine_dicts(old_error_data, error_so.error_data)
            _need_exc_info = False

        elif isinstance(exception, starlette.exceptions.HTTPException):
            status_code = exception.status_code
            if status_code in (starlette.status.HTTP_403_FORBIDDEN, starlette.status.HTTP_401_UNAUTHORIZED):
                error_so.error_code = ErrorSO.APIErrorCodes.cannot_authorize
                _need_exc_info = False
            elif status_code == starlette.status.HTTP_404_NOT_FOUND:
                error_so.error_code = ErrorSO.APIErrorCodes.not_found
                _need_exc_info = False
            else:
                status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
                _need_exc_info = True
            with suppress(Exception):
                error_so.error_data["exception.detail"] = exception.detail

        elif isinstance(exception, fastapi.exceptions.RequestValidationError):
            status_code = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
            error_so.error_code = ErrorSO.APIErrorCodes.error_in_request
            with suppress(Exception):
                error_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}
            _need_exc_info = False

        else:
            status_code = starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            error_so.error_code = ErrorSO.APIErrorCodes.unknown_error
            _logger.exception(exception)
            _need_exc_info = True

        if error_so.error_code:
            error_so.error_code = error_so.error_code.upper().replace(" ", "_").strip()

        if error_so.error_code_specification:
            error_so.error_code_specification = (
                error_so.error_code_specification.upper().replace(" ", "_").strip()
            )

        if _need_exc_info:
            _logger.error(str(exception), exc_info=exception)
        else:
            _logger.error(str(exception))

        _kwargs = {}
        for func in funcs_before_response:
            _func_data = func(
                status_code=status_code, error_so=error_so, request=request, exception=exception, **_kwargs
            )
            if asyncio.iscoroutine(_func_data):
                _func_data = await _func_data
            if _func_data is not None:
                status_code, error_so, _kwargs = _func_data[0], _func_data[1], _func_data[2]
                raise_for_type(status_code, int)
                raise_for_type(error_so, ErrorSO)
                raise_for_type(_kwargs, dict)

        for async_func_after_response in async_funcs_after_response:
            raise_if_not_async_func(async_func_after_response)
            _ = asyncio.create_task(async_func_after_response(
                error_so=error_so, status_code=status_code, request=request, exception=exception
            ))

        return APIJSONResponse(
            content=error_so,
            status_code=status_code
        )

    return handle_exception


def create_handle_exception_creating_story_log(
        *,
        sqlalchemy_db: SQLAlchemyDB
) -> Callable:
    def handle_exception(
            *,
            status_code: int,
            error_so: ErrorSO,
            request: starlette.requests.Request,
            exception: Exception,
            **kwargs
    ) -> (int, ErrorSO, dict[str, Any]):
        sqlalchemy_db.init()
        traceback_str = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        with sqlalchemy_db.new_session() as session:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                title=str(exception),
                data={
                    "error_so": error_so.model_dump(),
                    "traceback_str": traceback_str
                }
            )
            session.add(story_log_dbm)
            session.commit()
            session.refresh(story_log_dbm)
        error_so.error_data.update({"story_log_long_id": story_log_dbm.long_id})
        kwargs["story_log_id"] = story_log_dbm.id
        return status_code, error_so, kwargs

    return handle_exception


def add_exception_handler_to_app(*, app: FastAPI, handle_exception: Callable) -> FastAPI:
    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=ValueError,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=handle_exception
    )
    app.add_exception_handler(
        exc_class_or_status_code=starlette.exceptions.HTTPException,
        handler=handle_exception
    )
    return app


def add_swagger_to_app(
        *,
        app: FastAPI,
        favicon_url: str | None = None
):
    app.mount(
        "/ar_fastapi_static",
        StaticFiles(directory=os.path.join(str(pathlib.Path(__file__).parent), "ar_fastapi_static")),
        name="ar_fastapi_static"
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title,
            swagger_js_url="/ar_fastapi_static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/ar_fastapi_static/swagger-ui/swagger-ui.css",
            swagger_favicon_url=favicon_url
        )

    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title,
            redoc_js_url="/ar_fastapi_static/redoc/redoc.standalone.js",
            redoc_favicon_url=favicon_url
        )

    return app


def add_cors_to_app(*, app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def add_needed_api_router_to_app(*, app: FastAPI):
    api_router = APIRouter()

    @api_router.get(
        "/healthcheck",
        response_model=ErrorSO,
        status_code=starlette.status.HTTP_200_OK,
        tags=["Healthcheck"]
    )
    async def _():
        return APIJSONResponse(
            status_code=starlette.status.HTTP_200_OK,
            content=RawDataSO(data={"healthcheck": "healthcheck"})
        )

    @api_router.get(
        "/arpakitlib",
        response_model=ErrorSO,
        status_code=starlette.status.HTTP_200_OK,
        tags=["arpakitlib"]
    )
    async def _():
        return APIJSONResponse(
            status_code=starlette.status.HTTP_200_OK,
            content=RawDataSO(data={"arpakitlib": "arpakitlib"})
        )

    app.include_router(router=api_router, prefix="")

    return app


class BaseStartupAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_startup(self, *args, **kwargs):
        self._logger.info("on_startup starts")
        self._logger.info("on_startup ends")


class BaseShutdownAPIEvent:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    async def async_on_shutdown(self, *args, **kwargs):
        self._logger.info("on_shutdown starts")
        self._logger.info("on_shutdown ends")


class InitSqlalchemyDBStartupAPIEvent(BaseStartupAPIEvent):
    def __init__(self, sqlalchemy_db: SQLAlchemyDB):
        super().__init__()
        self.sqlalchemy_db = sqlalchemy_db

    def async_on_startup(self, *args, **kwargs):
        self.sqlalchemy_db.init()


class SyncSafeRunWorkerStartupAPIEvent(BaseStartupAPIEvent):
    def __init__(self, worker: BaseWorker):
        super().__init__()
        self.worker = worker

    def async_on_startup(self, *args, **kwargs):
        thread = threading.Thread(
            target=self.worker.sync_safe_run,
            daemon=True
        )
        thread.start()


class AsyncSafeRunWorkerStartupAPIEvent(BaseStartupAPIEvent):
    def __init__(self, worker: ExecuteOperationWorker):
        super().__init__()
        self.worker = worker

    def async_on_startup(self, *args, **kwargs):
        _ = asyncio.create_task(self.worker.async_safe_run())


class BaseTransmittedAPIData(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)


def get_transmitted_api_data(request: starlette.requests.Request) -> BaseTransmittedAPIData:
    return request.app.state.transmitted_api_data


def simple_api_router_for_testing():
    router = APIRouter(tags=["Testing"])

    @router.get(
        "/raise_fake_exception_1",
        response_model=ErrorSO
    )
    async def _():
        raise fastapi.HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.get(
        "/raise_fake_exception_2",
        response_model=ErrorSO
    )
    async def _():
        raise APIException(
            error_code="raise_fake_exception_2",
            error_code_specification="raise_fake_exception_2",
            error_description="raise_fake_exception_2"
        )

    @router.get(
        "/raise_fake_exception_3",
        response_model=ErrorSO
    )
    async def _():
        raise Exception("raise_fake_exception_3")

    @router.get(
        "/check_params",
        response_model=ErrorSO
    )
    async def _(name: int = Query()):
        return RawDataSO(data={"name": name})

    return router


def create_fastapi_app(
        *,
        title: str = "arpakitlib FastAPI",
        description: str | None = "arpakitlib FastAPI",
        log_filepath: str | None = "./story.log",
        handle_exception_: Callable | None = create_handle_exception(),
        startup_api_events: list[BaseStartupAPIEvent] | None = None,
        shutdown_api_events: list[BaseStartupAPIEvent] | None = None,
        transmitted_api_data: BaseTransmittedAPIData = BaseTransmittedAPIData(),
        api_router: APIRouter = simple_api_router_for_testing()
):
    setup_normal_logging(log_filepath=log_filepath)

    if not startup_api_events:
        startup_api_events = [BaseStartupAPIEvent()]

    if not shutdown_api_events:
        shutdown_api_events = [BaseShutdownAPIEvent()]

    app = FastAPI(
        title=title,
        description=description,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi",
        on_startup=[api_startup_event.async_on_startup for api_startup_event in startup_api_events],
        on_shutdown=[api_shutdown_event.async_on_shutdown for api_shutdown_event in shutdown_api_events]
    )

    app.state.transmitted_api_data = transmitted_api_data

    add_cors_to_app(app=app)

    add_swagger_to_app(app=app)

    if handle_exception_:
        add_exception_handler_to_app(
            app=app,
            handle_exception=handle_exception_
        )
    else:
        add_exception_handler_to_app(
            app=app,
            handle_exception=create_handle_exception()
        )

    add_needed_api_router_to_app(app=app)

    app.include_router(router=api_router)

    return app


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
