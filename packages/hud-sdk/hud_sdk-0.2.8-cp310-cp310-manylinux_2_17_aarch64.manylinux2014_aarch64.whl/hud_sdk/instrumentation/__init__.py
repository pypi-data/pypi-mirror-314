import sys
import types
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import find_spec
from typing import Dict, Optional, Sequence, Set  # noqa: F401

from .base_instrumentation import BaseInstrumentation  # noqa: F401


class ModuleInstrumentor:
    def __init__(self) -> None:
        from .django.django_instrumentation import DjangoInstrumentation
        from .fastapi_instrumentation import FastApiInstrumentation
        from .flask_instrumentation import FlaskInstrumentation

        django_instrumentation = DjangoInstrumentation()
        flask_instrumentation = FlaskInstrumentation()
        fastapi_instrumentation = FastApiInstrumentation()

        self.instrumentations = {
            flask_instrumentation.module_name: flask_instrumentation,
            fastapi_instrumentation.module_name: fastapi_instrumentation,
            django_instrumentation.module_name: django_instrumentation,
        }  # type: Dict[str, BaseInstrumentation]

    def instrument_module(self, module: types.ModuleType) -> None:
        module_name = module.__name__
        instrumentation = self.instrumentations.get(module_name, None)
        if instrumentation:
            instrumentation.instrument()


class ImportHookLoader(Loader):
    def __init__(
        self,
        instrumentor: ModuleInstrumentor,
        original_loader: Loader,
    ) -> None:
        self.instrumentor = instrumentor
        self.original_loader = original_loader

    def create_module(self, spec: ModuleSpec) -> Optional[types.ModuleType]:
        if self.original_loader and hasattr(self.original_loader, "create_module"):
            return self.original_loader.create_module(spec)
        # Return None to let the default module creation happen
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        if self.original_loader and hasattr(self.original_loader, "exec_module"):
            self.original_loader.exec_module(module)
        self.instrumentor.instrument_module(module)


class ImportHookFinder(MetaPathFinder):
    def __init__(self, instrumentor: ModuleInstrumentor):
        self.instrumentor = instrumentor
        self.in_progess = set()  # type: Set[str]

    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[str]] = None,
        target: Optional[types.ModuleType] = None,
    ) -> Optional[ModuleSpec]:
        if fullname in self.in_progess:
            # The find_spec from importlib will call us again, so we need to avoid infinite recursion
            return None

        self.in_progess.add(fullname)
        try:
            if fullname in self.instrumentor.instrumentations:
                spec = find_spec(fullname)  # Find the right module spec
                if spec is not None:
                    loader = getattr(spec, "loader", None)
                    if loader and not isinstance(loader, ImportHookLoader):
                        loader = ImportHookLoader(self.instrumentor, loader)
                        spec.loader = loader
                        return spec
        finally:
            self.in_progess.remove(fullname)
        return None  # Return None to let the default spec finding happen


def instrument_frameworks() -> None:
    instrumentor = ModuleInstrumentor()
    sys.meta_path.insert(0, ImportHookFinder(instrumentor))

    # Instrument already loaded modules
    for instrumentation in instrumentor.instrumentations.values():
        if instrumentation.module_name in sys.modules:
            instrumentation.instrument()
