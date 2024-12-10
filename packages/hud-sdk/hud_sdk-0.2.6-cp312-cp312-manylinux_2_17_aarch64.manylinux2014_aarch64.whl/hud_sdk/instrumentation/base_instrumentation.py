import importlib
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from ..logging import internal_logger


def parse_version(version: str) -> Optional[Tuple[int, ...]]:
    """Convert a semantic version string into a tuple of integers."""
    try:
        return tuple(map(int, (version.split(".") + ["0", "0"])[:3]))
    except Exception:
        internal_logger.error(
            "Could not parse version string", data={"version": version}
        )
        return None


class BaseInstrumentation(ABC):
    def __init__(
        self,
        module_name: str,
        package_name: str,
        minimum_version: str,
        maximum_version: Optional[str],
    ):
        self.module_name = module_name
        self.package_name = package_name
        self.minimum_version = parse_version(minimum_version)
        self.maximum_version = (
            parse_version(maximum_version) if maximum_version else None
        )

    def get_module_version(self) -> Optional[str]:
        try:
            from importlib.metadata import version

            return version(self.package_name)
        except Exception:
            pass

        try:
            module = importlib.import_module(self.module_name)
            return getattr(module, "__version__", None)
        except Exception:
            internal_logger.error(
                "Could not get the version of module", data={"module": self.module_name}
            )
            return None

    def is_enabled(self) -> bool:
        return True

    def is_supported(self) -> bool:
        version_str = self.get_module_version()
        if version_str is None:
            internal_logger.error(
                "Could not get the version of module", data={"module": self.module_name}
            )
            return False

        current_version = parse_version(version_str)
        if current_version is None:
            return False

        if self.minimum_version is not None and current_version < self.minimum_version:
            internal_logger.error(
                "Module version is not supported",
                data={
                    "module": self.module_name,
                    "version": current_version,
                    "minimum_version": self.minimum_version,
                },
            )
            return False

        if self.maximum_version is not None and current_version > self.maximum_version:
            internal_logger.error(
                "Module version is not supported",
                data={
                    "module": self.module_name,
                    "version": current_version,
                    "maximum_version": self.maximum_version,
                },
            )
            return False

        return True

    def instrument(self) -> None:
        if not self.is_enabled():
            internal_logger.info(
                "Instrumentation is disabled", data={"module": self.module_name}
            )
            return
        if not self.is_supported():
            return
        try:
            self._instrument()
            internal_logger.info(
                "Instrumented successfully", data={"module": self.module_name}
            )
        except Exception:
            internal_logger.exception(
                "Failed to instrument", data={"module": self.module_name}
            )

    @abstractmethod
    def _instrument(self) -> None:
        pass
