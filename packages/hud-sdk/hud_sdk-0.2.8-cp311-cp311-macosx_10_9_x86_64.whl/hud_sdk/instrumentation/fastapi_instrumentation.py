from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    List,
    Optional,
    Set,
    Type,  # noqa: F401
    Union,
    cast,
)

from hud_sdk.instrumentation.metaclass import overrideclass

from ..config import config
from ..endpoint_manager import EndpointManager
from ..flow_metrics import EndpointMetric
from ..logging import internal_logger
from ..native import set_flow_id
from ..utils import mark_linked_function
from .base_instrumentation import BaseInstrumentation

if TYPE_CHECKING:
    import fastapi  # noqa: F401
    from starlette.routing import BaseRoute  # noqa: F401
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

    Handle = Callable[[Any, Scope, Receive, Send], Awaitable[None]]


PREFIX_ATTR = "__hud_prefix"
FLOW_ID_ATTR = "__hud_flow_id"


class AsgiEndpointMetricsMiddleware:
    def __init__(self, app: "ASGIApp") -> None:
        self.app = app

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        metric = EndpointMetric()
        metric.start()

        def wrap_send(send: "Send") -> "Send":
            @wraps(send)
            async def wrapped_send(message: "Message") -> None:
                try:
                    if message.get("type") == "http.response.start":
                        metric.set_response_attributes(message["status"])
                except Exception:
                    internal_logger.exception(
                        "An error occurred in setting the response attributes"
                    )
                await send(message)

            return wrapped_send

        await self.app(scope, receive, wrap_send(send))

        try:
            metric.stop()
            route = scope.get("route")
            if not route:
                path = scope.get("path", "")
                internal_logger.info(
                    "Cannot send endpoint metrics because route is not found",
                    data={"path": path},
                )
                return

            flow_id = getattr(route, FLOW_ID_ATTR, None)
            metric.flow_id = flow_id

            path = route.path
            method = scope.get("method", "")
            if path and method:
                metric.set_request_attributes(path, method)
                metric.save()
            else:
                internal_logger.info(
                    "Cannot send endpoint metrics because path or method is not found",
                    data={"path": path, "method": method},
                )

        except Exception:
            internal_logger.exception("An error occurred in sending endpoint metrics")


def _mark_middlewares(fastapi_app: "fastapi.FastAPI") -> None:
    from starlette.middleware.base import BaseHTTPMiddleware

    for middleware in fastapi_app.user_middleware:
        # Special casae for BaseHTTPMiddleware, which are created by `@app.middleware("http")`.
        # This class has a `dispatch` method which is the user-defined function.
        if isinstance(middleware.cls, type) and issubclass(
            middleware.cls, BaseHTTPMiddleware
        ):
            if hasattr(middleware, "kwargs"):
                dispatch = middleware.kwargs.get("dispatch", None)
                if dispatch:
                    mark_linked_function(dispatch)  # type: ignore
            if hasattr(middleware, "options"):
                dispatch = middleware.options.get("dispatch", None)
                if dispatch:
                    mark_linked_function(dispatch)  # type: ignore
        else:
            mark_linked_function(middleware.cls)


class FastApiInstrumentation(BaseInstrumentation):
    def __init__(self) -> None:
        super().__init__(
            "fastapi", "fastpi", "0.75.0", None
        )  # Only in this version the route was added
        self.endpoint_manager = EndpointManager()
        self.instrumented_fast_api_class = None  # type: Optional[Type[fastapi.FastAPI]]
        self.instrumented_router_class = None  # type: Optional[Type[fastapi.APIRouter]]

    def is_enabled(self) -> bool:
        return config.instrument_fastapi

    def _save_endpoint_declarations_for_routes(
        self, routes: List["BaseRoute"], prefix: str = ""
    ) -> None:
        from starlette.routing import Mount, Route

        for route in routes:
            if isinstance(route, Route):
                existing_flow_id = getattr(route, FLOW_ID_ATTR, None)

                path = prefix + route.path
                methods = route.methods
                framework = self.module_name

                flow_id = self.endpoint_manager.save_endpoint_declaration(
                    path, list(methods) if methods else [], framework, existing_flow_id
                )
                if existing_flow_id is None:
                    setattr(route, FLOW_ID_ATTR, flow_id)
                mark_linked_function(route.endpoint)
                continue
            elif isinstance(route, Mount):
                # We want to validate that the app is a FastAPI app and the router is a FastAPI router,
                # since the `mount` method can be used with any ASGI app.
                if self.instrumented_fast_api_class and isinstance(
                    route.app, self.instrumented_fast_api_class
                ):
                    if self.instrumented_router_class and isinstance(
                        route.app.router, self.instrumented_router_class
                    ):
                        new_prefix = prefix + route.path
                        self._save_endpoint_declarations_for_router(
                            route.app.router, new_prefix
                        )
                continue

    def _save_endpoint_declarations_for_router(
        self, router: "fastapi.APIRouter", prefix: str = ""
    ) -> None:
        prefix = prefix + router.prefix
        setattr(router, PREFIX_ATTR, prefix)
        self._save_endpoint_declarations_for_routes(router.routes, prefix)

    def _instrument(self_instrument) -> None:
        import fastapi

        class InstumentedFastAPI(
            fastapi.FastAPI, metaclass=overrideclass(inherit_class=fastapi.FastAPI)  # type: ignore[misc]
        ):
            async def __call__(
                self, scope: "Scope", receive: "Receive", send: "Send"
            ) -> None:
                # Saves the endpoint declarations and marks the middlewares for all the existing routes and middlewares.
                # The internal `_save_endpoint_declarations_for_router` sets the prefix attribute for the router, so we call it only once.
                try:
                    prefix = getattr(self.router, PREFIX_ATTR, None)
                    if prefix is None:
                        self_instrument._save_endpoint_declarations_for_router(
                            self.router
                        )

                        # Middleware cannot be added after the app is running, so we can do it only once here
                        _mark_middlewares(self)
                except Exception:
                    internal_logger.exception(
                        "An error occurred in saving endpoint declarations"
                    )

                await super().__call__(scope, receive, send)

            def build_middleware_stack(self) -> "ASGIApp":
                original_stack = super().build_middleware_stack()
                return AsgiEndpointMetricsMiddleware(original_stack)

        class InstrumentedRouter(
            fastapi.APIRouter, metaclass=overrideclass(inherit_class=fastapi.APIRouter)  # type: ignore[misc]
        ):
            def add_api_route(
                self,
                path: str,
                endpoint: Callable[..., Any],
                *,
                methods: Optional[Union[Set[str], List[str]]] = None,
                **kwargs: Any
            ) -> None:
                before_add = len(self.routes)
                # Calls the original add_api_route method, and saves the endpoint declarations for the new route
                super().add_api_route(path, endpoint, methods=methods, **kwargs)
                try:
                    prefix = getattr(self, PREFIX_ATTR, None)
                    if prefix is not None:
                        if len(self.routes) == before_add + 1:
                            self_instrument._save_endpoint_declarations_for_routes(
                                [self.routes[-1]], prefix
                            )
                        else:
                            internal_logger.warning(
                                "The number of routes after adding a new route is not as expected",
                                data={
                                    "before_add": before_add,
                                    "after_add": len(self.routes),
                                },
                            )
                except Exception:
                    internal_logger.warning(
                        "An error occurred in saving fastapi endpoint declarations",
                        exc_info=True,
                    )

            def __hud_validate_router_type(
                self, new_route: Any, path: str
            ) -> Optional["InstrumentedRouter"]:
                from starlette.routing import Mount

                if not isinstance(new_route, Mount):
                    internal_logger.warning(
                        "The new route is not an instance of Mount",
                        data={"path": path, "type": type(new_route)},
                    )
                    return None
                if not (
                    self_instrument.instrumented_fast_api_class
                    and isinstance(
                        new_route.app, self_instrument.instrumented_fast_api_class
                    )
                ):
                    internal_logger.warning(
                        "The new app is not an instance of InstrumentedFastAPI",
                        data={"path": path, "type": type(new_route.app)},
                    )
                    return None
                new_router = new_route.app.router
                if not (
                    self_instrument.instrumented_router_class
                    and isinstance(
                        new_router, self_instrument.instrumented_router_class
                    )
                ):
                    internal_logger.warning(
                        "The new router is not an instance of InstrumentedRouter",
                        data={"path": path, "type": type(new_router)},
                    )
                    return None
                return cast("InstrumentedRouter", new_router)

            def mount(
                self, path: str, app: "ASGIApp", name: Optional[str] = None
            ) -> None:
                # Calls the original mount method, and saves the endpoint declarations for the new router
                super().mount(path, app, name)

                try:
                    prefix = getattr(self, PREFIX_ATTR, None)
                    if prefix is None:
                        return

                    prefix += path
                    new_route = self.routes[-1]

                    new_router = self.__hud_validate_router_type(new_route, path)
                    if not new_router:
                        return

                    self_instrument._save_endpoint_declarations_for_router(
                        new_router, prefix
                    )
                except Exception:
                    internal_logger.warning(
                        "An error occurred in saving fastapi endpoint declarations for mount",
                        exc_info=True,
                        data={"path": path},
                    )

        def create_handle(original_handle: "Handle") -> "Handle":
            @wraps(original_handle)
            async def _handle(
                self: Any, scope: "Scope", receive: "Receive", send: "Send"
            ) -> None:
                flow_id_set = False
                try:
                    # Set the flow_id for the current request, and calls the original handle
                    flow_id = getattr(self, FLOW_ID_ATTR, None)
                    if flow_id is not None:
                        set_flow_id(flow_id)
                        flow_id_set = True
                except Exception:
                    internal_logger.exception(
                        "An error occurred in setting the flow_id"
                    )

                await original_handle(self, scope, receive, send)

                try:
                    if flow_id_set:
                        set_flow_id(None)
                except Exception:
                    internal_logger.exception(
                        "An error occurred in unsetting the flow_id"
                    )

            return _handle

        self_instrument.instrumented_fast_api_class = InstumentedFastAPI
        self_instrument.instrumented_router_class = InstrumentedRouter

        fastapi.FastAPI = InstumentedFastAPI  # type: ignore
        fastapi.routing.APIRouter = InstrumentedRouter  # type: ignore
        fastapi.routing.APIRoute.handle = create_handle(fastapi.routing.APIRoute.handle)  # type: ignore
