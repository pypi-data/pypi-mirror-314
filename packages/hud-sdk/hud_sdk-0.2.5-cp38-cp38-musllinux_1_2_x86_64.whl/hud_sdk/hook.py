import ast
import os
import sys
import time
import traceback
from hashlib import sha1
from importlib.abc import Loader, PathEntryFinder
from importlib.machinery import FileFinder, ModuleSpec, SourceFileLoader
from types import CodeType
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from ._internal import worker_queue
from .collectors.modules import get_loaded_modules
from .config import config
from .declarations import Declaration
from .exception_handler import install_exception_handler
from .instrumentation import instrument_frameworks
from .logging import internal_logger
from .native import set_hud_running_mode
from .run_mode import should_run_hud
from .schemas.events import ScopeNode, ScopeType
from .utils import calculate_uuid

FunctionDef = TypeVar("FunctionDef", ast.FunctionDef, ast.AsyncFunctionDef)

paths_to_wrap = [
    os.getcwd(),
]  # type: List[str]


def add_path_of_main_module() -> None:
    try:
        spec = getattr(sys.modules["__main__"], "__spec__", None)
        if not spec:
            add_path_of_main_file()
            return

        package = spec.name.split(".")[0]
        package_module = sys.modules.get(package)
        if not package_module:
            add_path_of_main_file()
            return

        package_file = getattr(package_module, "__file__", None)
        if not package_file:
            add_path_of_main_file()
            return

        paths_to_wrap.append(os.path.dirname(os.path.abspath(package_file)))
    except Exception:
        internal_logger.exception("Error while getting main module path")
        add_path_of_main_file()


def add_path_of_main_file() -> None:
    file_path = getattr(sys.modules["__main__"], "__file__", None)
    if file_path:
        paths_to_wrap.append(os.path.dirname(os.path.abspath(file_path)))


add_path_of_main_module()


class ScopeContextManager:
    def __init__(
        self,
        scope: List[ScopeNode],
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module],
        default_name: str = "",
    ) -> None:
        self.default_name = default_name
        self.scope = scope
        self.node = node

    def __enter__(self) -> None:
        if isinstance(self.node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scope_type = ScopeType.FUNCTION
        elif isinstance(self.node, ast.ClassDef):
            scope_type = ScopeType.CLASS
        elif isinstance(self.node, ast.Module):
            scope_type = ScopeType.MODULE
        else:
            raise TypeError("Invalid node type")

        self.scope.append(
            ScopeNode(scope_type, getattr(self.node, "name", self.default_name))
        )

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.scope.pop()


class ASTTransformer(ast.NodeTransformer):
    def __init__(self, path: str, module_name: str, lines: List[bytes]) -> None:
        self.path = path
        self.module_name = module_name
        self.lines = lines
        self.compiler_flags = 0
        self.scope = []  # type: List[ScopeNode]

    def get_function_source_code_hash(
        self, node: Union[ast.stmt, ast.expr, ast.mod]
    ) -> str:
        if (sys.version_info.major, sys.version_info.minor) < (3, 8):
            return sha1(ast.dump(node).encode()).hexdigest()
        else:
            start_line = getattr(node, "lineno", 1) - 1
            end_line = cast(int, getattr(node, "end_lineno", 1)) - 1
            source_code = b"\n".join(self.lines[start_line : end_line + 1])
            return sha1(source_code).hexdigest()

    @staticmethod
    def get_and_remove_docstring(
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Optional[ast.stmt]:
        """
        If the first expression in the function is a literal string (docstring), remove it and return it
        """

        AstStrType = ast.Constant if sys.version_info >= (3, 8) else ast.Str

        if not node.body:
            return None
        if (
            isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, AstStrType)
            and (
                isinstance(node.body[0].value.value, str)
                if sys.version_info >= (3, 8)
                else isinstance(node.body[0].value.s, str)
            )
        ):
            return node.body.pop(0)
        return None

    def scope_manager(
        self,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module],
        default_name: str = "",
    ) -> ScopeContextManager:
        return ScopeContextManager(self.scope, node, default_name)

    @staticmethod
    def get_with_location_from_node(node: FunctionDef) -> Dict[str, int]:
        if len(node.body) == 0:
            return {
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "end_lineno": getattr(node, "end_lineno", node.lineno),
                "end_col_offset": getattr(node, "end_col_offset", node.col_offset),
            }

        return {
            "lineno": node.body[0].lineno,
            "col_offset": node.body[0].col_offset,
            "end_lineno": getattr(node.body[0], "end_lineno", node.body[0].lineno),
            "end_col_offset": getattr(
                node.body[0], "end_col_offset", node.body[0].col_offset
            ),
        }

    def get_with_stmt(self, function_id: str, node: FunctionDef) -> ast.With:
        locations = self.get_with_location_from_node(node)

        args = []  # type: List[ast.expr]
        if sys.version_info < (3, 6):
            args = [ast.Str(function_id, **locations)]
        else:
            args = [ast.Constant(value=function_id, kind=None, **locations)]
        return ast.With(
            items=[
                ast.withitem(
                    context_expr=ast.Call(
                        func=ast.Name(id="HudMonitor", ctx=ast.Load(), **locations),
                        args=args,
                        keywords=[],
                        **locations,
                    ),
                )
            ],
            body=[],
            type_comment=None,
            **locations,
        )

    def _visit_generic_FunctionDef(self, node: FunctionDef) -> FunctionDef:
        source_code_hash = self.get_function_source_code_hash(node)
        function_id = calculate_uuid(
            "{}|{}|{}".format(node.name, self.path, Declaration.get_lineno(node))
        )

        if isinstance(node, ast.FunctionDef):
            is_async = False
        elif isinstance(node, ast.AsyncFunctionDef):
            is_async = True
        else:
            raise TypeError("Invalid node type")

        worker_queue.append(
            Declaration.from_function_node(
                function_id,
                node,
                source_code_hash,
                self.path,
                is_async=is_async,
                scope=self.scope,
            )
        )

        with self.scope_manager(node):
            docstring = self.get_and_remove_docstring(node)

            with_stmt = self.get_with_stmt(str(function_id), node)
            with_stmt.body = node.body

            if not with_stmt.body:
                with_stmt.body = [ast.Pass(**self.get_with_location_from_node(node))]

            if docstring is not None:
                node.body = [docstring, with_stmt]
            else:
                node.body = [with_stmt]

            self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        return self._visit_generic_FunctionDef(node)

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        return self._visit_generic_FunctionDef(node)

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        node.args = self.visit(node.args)
        node.body = self.visit(node.body)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        source_code_hash = self.get_function_source_code_hash(node)
        class_id = calculate_uuid(
            "{}|{}|{}".format(node.name, self.path, Declaration.get_lineno(node))
        )
        worker_queue.append(
            Declaration.from_class_node(
                class_id, node, source_code_hash, self.path, scope=self.scope
            )
        )
        with self.scope_manager(node):
            self.generic_visit(node)
            return node

    def visit_Module(self, node: ast.Module) -> Any:
        source_code_hash = self.get_function_source_code_hash(node)
        module_id = calculate_uuid(self.path)
        worker_queue.append(
            Declaration.from_module_node(module_id, node, source_code_hash, self.path)
        )

        with self.scope_manager(node, default_name=self.module_name):
            self.generic_visit(node)
            return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Optional[ast.ImportFrom]:
        # When passing an AST to the `compile` function, the `__future__` imports are not parsed
        # and the compiler flags are not set. This is a workaround to set the compiler flags,
        # and removing the invalid imports.
        if node.module == "__future__":
            import __future__

            for name in node.names:
                feature = getattr(__future__, name.name)
                self.compiler_flags |= feature.compiler_flag
            return None

        self.generic_visit(node)
        return node


def should_wrap_file(path: str) -> bool:
    return path in paths_to_wrap


def should_wrap_module(fullname: str) -> bool:
    if fullname in config.modules_to_trace:
        return True
    for module in config.modules_to_trace:
        if fullname.startswith("{}.".format(module)):
            return True
    return False


class MyFileFinder(FileFinder):
    def __repr__(self) -> str:
        return "MyFileFinder('{}')".format(self.path)

    def __init__(
        self,
        path: str,
        *loader_details: Tuple[Type[Loader], List[str]],
        override: bool = False
    ) -> None:
        if not should_wrap_file(os.path.abspath(path)) and not override:
            raise ImportError("Not wrapping path: {}".format(path))

        super().__init__(path, *loader_details)

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = super().find_spec(fullname, *args)
        if spec is not None and spec.submodule_search_locations is not None:
            paths_to_wrap.extend(spec.submodule_search_locations)
        return spec


class ModuleFinder(MyFileFinder):

    def __init__(self, path: str, original_finder: PathEntryFinder) -> None:
        self.path = path
        self.original_finder = original_finder

        if hasattr(original_finder, "_loaders"):
            suffixes = [loader[0] for loader in original_finder._loaders]
        else:
            raise ImportError("Original finder unsupported for path {}".format(path))

        if ".py" not in suffixes:
            raise ImportError("Not wrapping loader that doesn't handle .py files")

        loader_details = []

        if set(suffixes) == {".py"}:
            loader_details.append((MySourceLoader, [".py"]))
        else:
            for suffix, loader in original_finder._loaders:
                if suffix == ".py":
                    loader_details.append((MySourceLoader, [suffix]))
                else:
                    loader_details.append((loader, [suffix]))

        super().__init__(path, *loader_details, override=True)

    def __repr__(self) -> str:
        return "ModuleFinder('{}', original_finder={})".format(
            self.path, self.original_finder
        )

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = None
        if should_wrap_module(fullname):
            spec = super().find_spec(fullname, *args)
        if spec is not None:
            if spec.origin is not None and spec.origin not in paths_to_wrap:
                paths_to_wrap.append(os.path.dirname(spec.origin))
            return spec
        if self.original_finder is not None:
            return self.original_finder.find_spec(fullname, *args)


class MySourceLoader(SourceFileLoader):
    def path_stats(self, path: str) -> Mapping[str, Any]:
        if not path.endswith(".py"):
            return super().path_stats(path)
        stats = super().path_stats(path)
        # This manipulation allows bytecode caching to work for the edited module, without conflicting with the original module
        stats["mtime"] = time.time() * 2  # type: ignore[index]
        return stats

    def source_to_code(  # type: ignore[override]
        self, data: bytes, path: str, *, _optimize: int = -1
    ) -> CodeType:
        try:
            internal_logger.debug("Monitoring file: {}".format(path))
            tree = cast(
                ast.Module,
                compile(
                    data,
                    path,
                    "exec",
                    flags=ast.PyCF_ONLY_AST,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )  # type: ast.Module
            transformer = ASTTransformer(path, self.name, data.splitlines())
            tree = transformer.visit(tree)
            tree.body = [
                *ast.parse("from hud_sdk.native import Monitor as HudMonitor\n").body,
                *tree.body,
            ]

            return cast(
                CodeType,
                compile(
                    tree,
                    path,
                    "exec",
                    flags=transformer.compiler_flags,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )
        except Exception:
            internal_logger.exception(
                "Error while transforming AST on file", data={"path": path}
            )
            return super().source_to_code(data, path)


def module_hook(path: str) -> ModuleFinder:
    original_finder = None
    for hook in sys.path_hooks:
        if hook is not module_hook:
            try:
                original_finder = hook(path)
            except ImportError:
                continue
            return ModuleFinder(path, original_finder=original_finder)  # type: ignore[arg-type,unused-ignore]

    raise ImportError("No module finder found for path: {}".format(path))


def register_to_fork() -> None:
    if hasattr(os, "register_at_fork") and not config.run_after_fork:

        def _disable_hud() -> None:
            internal_logger.info(
                "Disabling HUD in child process"
            )  # It will print to the console if HUD_DEBUG is set
            set_hud_running_mode(False)
            # We don't clear the memory of main thread like the queue, aggs and logger, because of COW.
            # If we don't touch the memory, that's still "shared", but if we clear it, it copied and actually consomes more memory

        os.register_at_fork(after_in_child=_disable_hud)


hook_set = False


def set_hook() -> None:
    global hook_set
    if hook_set:
        return
    if should_run_hud():
        hook_set = True
        if not config.disable_exception_handler:
            install_exception_handler()

        internal_logger.info("Running config", data=config.__dict__)
        internal_logger.info(
            "Hook stacktrace", data={"stacktrace": traceback.format_stack()}
        )
        internal_logger.info("Loaded Modules", data=get_loaded_modules().to_json_data())

        for path in paths_to_wrap:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]
        for path in sys.path:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]

        loader_details = []
        if hasattr(sys.path_hooks[-1]("."), "_loaders"):
            for suffix, loader in sys.path_hooks[-1](".")._loaders:  # type: ignore[attr-defined]
                if suffix == ".py":
                    loader_details.append((MySourceLoader, [suffix]))
                else:
                    loader_details.append((loader, [suffix]))

        sys.path_hooks.insert(0, MyFileFinder.path_hook(*loader_details))
        sys.path_hooks.insert(0, module_hook)
        register_to_fork()
        instrument_frameworks()
    else:
        hook_set = True
