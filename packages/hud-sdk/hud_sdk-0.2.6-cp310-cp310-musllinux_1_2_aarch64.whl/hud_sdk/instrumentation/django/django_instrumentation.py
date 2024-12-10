import importlib
import inspect
from collections import defaultdict
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, List, NamedTuple, Optional, Set

from ...logging import internal_logger
from ...utils import mark_linked_function
from ..base_instrumentation import BaseInstrumentation
from . import endpoint_manager

if TYPE_CHECKING:
    from django.urls import URLPattern


def get_middleware_module() -> str:
    module_path = __name__.rsplit(".", 1)[0]
    return "{}.django_middleware.HudMiddleware".format(module_path)


MIDDLEWARE_MODULE = get_middleware_module()

URLMapping = NamedTuple(
    "URLMapping",
    [("path", str), ("view_func", Callable[..., Any]), ("methods", Set[str])],
)


class DjangoInstrumentation(BaseInstrumentation):
    def __init__(self) -> None:
        super().__init__("django", "django", "2.2.0", None)
        self.supported_http_methods = set()  # type: Set[str]

    def _instrument(self) -> None:
        import django

        if not self._is_middleware_exists():
            internal_logger.error(
                "Couldn't find our middleware module. Skipping instrumentation",
                data={"middleware_module": MIDDLEWARE_MODULE},
            )
            return

        original_django_setup = django.setup
        has_setup_ran = False

        @wraps(django.setup)
        def django_setup_wrapper(*args: Any, **kwargs: Any) -> Any:

            nonlocal has_setup_ran
            result = original_django_setup(*args, **kwargs)
            try:
                if not has_setup_ran:
                    from django.conf import settings
                    from django.urls import get_resolver
                    from django.views import View

                    self.supported_http_methods = {
                        method.upper() for method in View.http_method_names
                    }
                    self._extract_and_save_endpoints(get_resolver().url_patterns)

                    settings.MIDDLEWARE.insert(
                        0,
                        MIDDLEWARE_MODULE,
                    )
                has_setup_ran = True
            except Exception:
                internal_logger.exception("Error while extracting endpoints")
            return result

        django.setup = django_setup_wrapper

    def _is_middleware_exists(self) -> bool:
        try:
            package_name = MIDDLEWARE_MODULE.rsplit(".", 1)[0]
            class_name = MIDDLEWARE_MODULE.rsplit(".", 1)[1]
            package = importlib.import_module(package_name)
            if not hasattr(package, class_name):
                return False
        except ImportError:
            return False

        return True

    def _extract_and_save_endpoints(self, url_patterns: List[Any]) -> None:
        url_mappings = self._extract_url_mappings(url_patterns)
        for mapping in url_mappings:
            self._save_endpoint(mapping)

    def _save_endpoint(self, mapping: URLMapping) -> None:
        endpoint_manager.save_endpoint_declaration(
            path=mapping.path,
            methods=list(mapping.methods),
            framework=self.module_name,
        )
        mark_linked_function(mapping.view_func)

    def _extract_url_mappings(self, url_patterns: List[Any]) -> List[URLMapping]:
        from django.urls import URLPattern, URLResolver

        def traverse_patterns(
            pattern_list: List[Any],
            accumulated_path: str = "",
            url_mappings: Optional[List[URLMapping]] = None,
        ) -> List[URLMapping]:
            if not pattern_list:
                return []
            if url_mappings is None:
                url_mappings = []

            for pattern in pattern_list:
                if isinstance(pattern, URLPattern):
                    mappings = self._create_url_mappings(pattern, accumulated_path)
                    url_mappings.extend(mappings)
                elif isinstance(pattern, URLResolver):
                    traverse_patterns(
                        pattern.url_patterns,
                        accumulated_path + str(pattern.pattern),
                        url_mappings,
                    )
                else:
                    name = getattr(pattern, "__name__", None)
                    if name is None:
                        name = type(pattern).__name__

                    internal_logger.warning(
                        "Unknown pattern type", data={"pattern_name": name}
                    )
            return url_mappings

        return traverse_patterns(url_patterns)

    def _create_url_mappings(
        self, pattern: "URLPattern", accumulated_path: str
    ) -> List[URLMapping]:
        full_path = accumulated_path + str(pattern.pattern)
        view = pattern.callback
        if not callable(view):
            internal_logger.warning(
                "View function is not callable for path: {}".format(full_path)
            )
            return []

        method_handlers = self._get_view_method_handlers(view)
        url_mappings = []

        for handler, methods in method_handlers.items():
            url_mapping = URLMapping(
                path=full_path,
                view_func=handler,
                methods=methods,
            )
            url_mappings.append(url_mapping)

        return url_mappings

    def _get_view_method_handlers(
        self, view: Callable[..., Any]
    ) -> Dict[Callable[..., Any], Set[str]]:
        func_to_methods = defaultdict(set)  # type: Dict[Callable[..., Any], Set[str]]

        if hasattr(view, "view_class"):
            # Class-based view
            view_class = view.view_class
            method_handlers = self._get_method_handlers_from_class(view_class)
            for method_name, handler in method_handlers.items():
                func_to_methods[handler].add(method_name.upper())
        elif inspect.isfunction(view) or inspect.ismethod(view):
            supported_methods = self._get_supported_methods(view)
            func_to_methods[view] = supported_methods
        elif hasattr(view, "__call__"):
            view_class = view.__class__
            method_handlers = self._get_method_handlers_from_class(view_class)
            for method_name, handler in method_handlers.items():
                func_to_methods[handler].add(method_name.upper())
        else:
            internal_logger.warning("Unknown view type", data={"view": view})
            supported_methods = self.supported_http_methods
            func_to_methods[view] = supported_methods

        return func_to_methods

    def _get_supported_methods(self, view: Callable[..., Any]) -> Set[str]:
        if hasattr(view, "__closure__") and view.__closure__:
            # Using @require_http_methods decorator
            for cell in view.__closure__:
                cell_contents = cell.cell_contents
                if isinstance(cell_contents, list) and set(cell_contents).issubset(
                    self.supported_http_methods
                ):
                    # Assuming the decorator passes request_method_list as a list
                    return set(cell_contents)
        return self.supported_http_methods

    def _get_method_handlers_from_class(
        self, view_class: Any
    ) -> Dict[str, Callable[..., Any]]:
        method_handlers = {}
        for method_name in self.supported_http_methods:
            method_name_lower = method_name.lower()
            # Django class methods are in lower case
            if hasattr(view_class, method_name_lower):
                handler = getattr(view_class, method_name_lower)
                if callable(handler):
                    method_handlers[method_name] = handler
                else:
                    internal_logger.warning(
                        "handler is not callable",
                        data={"method_name": method_name, "handler": handler},
                    )
        return method_handlers
