from functools import wraps
from typing import Any, Callable, List, Tuple

from hud_sdk.instrumentation.metaclass import OverrideclassMetaclass

from ..config import config
from ..endpoint_manager import EndpointManager
from ..flow_metrics import EndpointMetric
from ..logging import internal_logger
from ..native import (
    set_flow_id,
)
from ..utils import mark_linked_function, suppress_exceptions_sync
from .base_instrumentation import BaseInstrumentation


class FlaskInstrumentation(BaseInstrumentation):

    def __init__(self) -> None:
        super().__init__("flask", "flask", "0.12.0", None)
        self.endpoint_manager = EndpointManager()

    def is_enabled(self) -> bool:
        return config.instrument_flask

    def _instrument(self) -> None:
        import flask

        @suppress_exceptions_sync(lambda: None)
        def _before_request() -> None:
            """
            This function is called before each request.
            We use it to set the flow_id for the current request.
            """
            if not flask.request.url_rule:
                return
            current_endpoint = flask.request.url_rule.rule
            current_method = flask.request.method

            current_flow_id = self.endpoint_manager.get_endpoint_id(
                current_endpoint, current_method
            )
            if current_flow_id is None:
                internal_logger.warning(
                    "Endpoint not found: {} with method: {}".format(
                        current_endpoint, current_method
                    )
                )
                return
            try:
                set_flow_id(current_flow_id)
            except Exception:
                internal_logger.exception("An error occurred in setting the flow_id")

        @suppress_exceptions_sync(lambda: None)
        def _extract_endpoints(app: Any) -> None:
            """
            This function is called for each request.
            We use it to extract all the endpoints of the application.
            We only do this once because Flask endpoints can't change during runtime.
            """
            if not app._hud_has_extracted_endpoints:
                app._hud_has_extracted_endpoints = True
                for rule in app.url_map.iter_rules():
                    self.endpoint_manager.save_endpoint_declaration(
                        path=rule.rule,
                        methods=list(rule.methods.difference({"HEAD", "OPTIONS"})),
                        framework=self.module_name,
                    )
                    view_func = app.view_functions.get(rule.endpoint)
                    if view_func:
                        mark_linked_function(view_func)

        @suppress_exceptions_sync(lambda: None)
        def _enrich_metric(metric: EndpointMetric, status: str) -> None:
            if flask.request.url_rule:
                current_endpoint = flask.request.url_rule.rule
                current_method = flask.request.method
                metric.flow_id = self.endpoint_manager.get_endpoint_id(
                    current_endpoint, current_method
                )
                metric.set_request_attributes(current_endpoint, current_method)
                metric.set_response_attributes(int(status.split()[0]))

        def _wrap_wsgi_app(
            original_wsgi_app: Callable[..., Any], app: Any
        ) -> Callable[..., Any]:
            @wraps(original_wsgi_app)
            def wsgi_app_wrapper(
                environ: Any, start_response: Callable[..., Callable[[bytes], object]]
            ) -> Any:
                """
                This function is called for each request.
                We use it to get an endpoint metric for the current request.
                Also, we extract all the endpoints of the application on the first request.
                """
                try:
                    _extract_endpoints(app)
                    metric = EndpointMetric()
                    metric.start()
                except Exception:
                    internal_logger.exception("An error occurred in wsgi_app_wrapper")

                def custom_start_response(
                    status: str, headers: List[Tuple[str, str]], *args: Any
                ) -> Callable[[bytes], object]:
                    _enrich_metric(metric, status)
                    return start_response(status, headers, *args)

                response = original_wsgi_app(environ, custom_start_response)
                try:
                    set_flow_id(None)
                    metric.stop()
                    metric.save()
                except Exception:
                    internal_logger.exception("An error occurred in wsgi_app_wrapper")
                finally:
                    return response

            return wsgi_app_wrapper

        def _before_request_wrapper(
            original_before_request: Callable[..., Callable[..., Any]]
        ) -> Callable[..., Any]:
            @wraps(original_before_request)
            def before_request_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
                try:
                    mark_linked_function(func)
                except Exception:
                    internal_logger.exception(
                        "An error occurred in flask before_request hook"
                    )
                finally:
                    return original_before_request(func)

            return before_request_wrapper

        class InstrumentedFlask(
            flask.Flask, metaclass=OverrideclassMetaclass, inherit_class=flask.Flask
        ):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                try:
                    self.before_request(_before_request)
                    self.before_request = _before_request_wrapper(self.before_request)  # type: ignore[method-assign]
                    self.wsgi_app = _wrap_wsgi_app(self.wsgi_app, self)  # type: ignore[method-assign]
                    self._hud_has_extracted_endpoints = False
                except Exception:
                    internal_logger.exception(
                        "An error occurred in flask __init__ hook"
                    )

        class InstrumentedBlueprint(
            flask.Blueprint,
            metaclass=OverrideclassMetaclass,
            inherit_class=flask.Blueprint,
        ):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                try:
                    self.before_request = _before_request_wrapper(self.before_request)  # type: ignore[method-assign]
                    self.before_app_request = _before_request_wrapper(self.before_app_request)  # type: ignore[method-assign]
                except Exception:
                    internal_logger.exception(
                        "An error occurred in blueprint __init__ hook"
                    )

        flask.Flask = InstrumentedFlask  # type: ignore[misc]
        flask.Blueprint = InstrumentedBlueprint  # type: ignore[misc]
