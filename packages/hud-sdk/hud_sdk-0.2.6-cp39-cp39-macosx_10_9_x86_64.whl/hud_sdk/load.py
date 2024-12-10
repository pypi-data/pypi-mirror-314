import inspect
import re
import sys
from typing import List, Optional

from .config import config
from .logging import internal_logger

did_load = False


def load_hud() -> None:
    global did_load
    if did_load:
        return
    did_load = True
    try:
        frames = inspect.stack()
        trace_importing_module(frames)
    except Exception:
        internal_logger.exception("Error while loading HUD")


def trace_importing_module(frames: List[inspect.FrameInfo]) -> None:
    try:
        importing_module = find_importing_module(frames)
        if not importing_module:
            internal_logger.warning("No importing module found")
            return
        top_level_module = importing_module.split(".")[0]
        if (
            top_level_module in config.modules_to_trace
            or top_level_module
            == "__main__"  # This is a special case, we already add the main module's file to the paths_to_wrap
        ):
            internal_logger.info(
                "Module is already configured in modules_to_trace",
                data={
                    "module": top_level_module,
                    "modules_to_trace": config.modules_to_trace,
                },
            )
            return

        config.modules_to_trace.append(top_level_module)
        internal_logger.info(
            "Added module to trace",
            data={
                "module": top_level_module,
                "modules_to_trace": config.modules_to_trace,
            },
        )
        if top_level_module != importing_module:
            internal_logger.info(
                "Module is not top level", data={"module": importing_module}
            )
        log_untraced_modules(top_level_module, importing_module)
    except Exception:
        internal_logger.exception("Error while tracing importing module")


def find_importing_module(frames: List[inspect.FrameInfo]) -> Optional[str]:
    """
    Iterates through the stack frames and find the code that imports the SDK
    """
    import_statements = re.compile(r"\s*(from|import)\s+{}".format(config.sdk_name))
    for frame in frames:
        if not frame.code_context:
            continue

        for line in frame.code_context:
            if not import_statements.match(line):
                continue
            module_name = frame.frame.f_globals.get("__name__", "")
            if (
                module_name
                and config.sdk_name not in module_name
                and module_name not in config.blacklisted_modules
            ):
                return module_name  # type: ignore[no-any-return]
    return None


def log_untraced_modules(top_level_module: str, importing_module: str) -> None:
    submodules = [top_level_module]
    prefix = top_level_module + "."
    for module_name in sys.modules:
        if module_name.startswith(prefix) and module_name != importing_module:
            submodules.append(module_name)

    internal_logger.info(
        "Untraced modules",
        data={"top_level_module": top_level_module, "submodules": submodules},
    )
