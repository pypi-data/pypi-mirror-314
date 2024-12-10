import asyncio
import mmap
import multiprocessing
import os
import tempfile
import time
import uuid
from functools import wraps
from multiprocessing.managers import BaseManager, BaseProxy
from threading import Lock, get_ident
from typing import (
    Any,
    BinaryIO,
    Callable,
    Coroutine,
    Dict,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from ...process_utils import get_current_pid
from ...run_mode import disable_hud
from ...utils import send_fatal_error


class OwnedLock:
    """
    This class implements a lock, with the addition of an owner field.
    """

    def __init__(self) -> None:
        self._block = Lock()
        self._owner = None  # type: Union[int, Tuple[int, int], None]
        self._lock_time = 0.0

    def _at_fork_reinit(self) -> None:
        self._block._at_fork_reinit()  # type: ignore[attr-defined]
        self._owner = None
        self._lock_time = 0.0

    def acquire(
        self,
        blocking: bool = True,
        timeout: int = -1,
        *,
        ident: Optional[Tuple[int, int]] = None,
    ) -> bool:
        """Acquire a lock, blocking or non-blocking."""
        rc = self._block.acquire(blocking, timeout)
        if rc:
            if ident:
                me = ident  # type: Union[int, Tuple[int, int]]
            else:
                me = get_ident()
            self._owner = me
            self._lock_time = time.time()
        return rc

    def release(self, *, ident: Optional[Tuple[int, int]] = None) -> None:
        """Release a lock."""
        if ident:
            me = ident  # type: Union[int, Tuple[int, int]]
        else:
            me = get_ident()
        if self._owner != me:
            raise RuntimeError("cannot release un-acquired lock")
        self._lock_time = 0.0
        self._owner = None
        self._block.release()

    def get_owner_and_locktime(
        self,
    ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]:
        if self._owner is None:
            return None
        return self._owner, self._lock_time


T = TypeVar("T")


@overload
def safe_manager_call(
    func: Callable[..., Coroutine[Any, Any, T]]
) -> Callable[..., Coroutine[Any, Any, T]]: ...


@overload
def safe_manager_call(func: Callable[..., T]) -> Callable[..., T]: ...


def safe_manager_call(
    func: Callable[..., T]
) -> Union[Callable[..., T], Callable[..., Coroutine[Any, Any, T]]]:
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)  # type: ignore[no-any-return]
            except AttributeError:
                # Used for hasattr checks
                raise
            except Exception:
                send_fatal_error(message="Exception in manager call")
                disable_hud(should_dump_logs=False, should_clear=False)
                raise

    else:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except AttributeError:
                # Used for hasattr checks
                raise
            except Exception:
                send_fatal_error(message="Exception in manager call")
                disable_hud(should_dump_logs=False, should_clear=False)
                raise

    return wrapper


# These proxy classes are defined, but not exported in multiprocessing.managers. We modify them.
class AcquirerProxy(BaseProxy):
    _exposed_ = ("acquire", "release", "get_owner_and_locktime")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ident = (get_current_pid(), get_ident())

    @safe_manager_call
    def acquire(self, blocking: bool = True, timeout: Optional[int] = None) -> bool:
        args = (blocking,) if timeout is None else (blocking, timeout)
        return self._callmethod("acquire", args, kwds={"ident": self.ident})  # type: ignore[func-returns-value, no-any-return]

    @safe_manager_call
    async def async_acquire(
        self, blocking: bool = True, timeout: Optional[int] = None
    ) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.acquire, blocking, timeout)

    @safe_manager_call
    def release(self) -> None:
        return self._callmethod("release", kwds={"ident": self.ident})

    @safe_manager_call
    async def async_release(self) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.release)

    @safe_manager_call
    def get_owner_and_locktime(
        self,
    ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]:
        return self._callmethod("get_owner_and_locktime")  # type: ignore[func-returns-value,no-any-return]

    @safe_manager_call
    async def async_get_owner_and_locktime(
        self,
    ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_owner_and_locktime)

    @safe_manager_call
    def __enter__(self) -> bool:
        return self.acquire()

    @safe_manager_call
    async def __aenter__(self) -> bool:
        return await self.async_acquire()

    @safe_manager_call
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        return self.release()

    @safe_manager_call
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.async_release()


class NamespaceProxy(BaseProxy):
    _exposed_ = ("__getattribute__", "__setattr__", "__delattr__")

    @safe_manager_call
    def __getattr__(self, key: str) -> Any:
        if key[0] == "_":
            return object.__getattribute__(self, key)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__getattribute__", (key,))

    @safe_manager_call
    def __setattr__(self, key: str, value: Any) -> None:
        if key[0] == "_":
            return object.__setattr__(self, key, value)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__setattr__", (key, value))  # type: ignore[no-any-return]

    @safe_manager_call
    def __delattr__(self, key: str) -> None:
        if key[0] == "_":
            return object.__delattr__(self, key)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__delattr__", (key,))  # type: ignore[no-any-return]


class EventProxy(BaseProxy):
    _exposed_ = ("is_set", "set", "clear", "wait")

    @safe_manager_call
    def is_set(self) -> bool:
        return self._callmethod("is_set")  # type: ignore[func-returns-value,no-any-return]

    @safe_manager_call
    def set(self) -> None:
        return self._callmethod("set")

    @safe_manager_call
    def clear(self) -> None:
        return self._callmethod("clear")

    @safe_manager_call
    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._callmethod("wait", (timeout,))  # type: ignore[func-returns-value,no-any-return]


class SharedMemoryContext:
    def __init__(self, mmap_obj: mmap.mmap, file_obj: BinaryIO, file_name: str) -> None:
        self.mmap_obj = mmap_obj
        self.file_obj = file_obj
        self.file_name = file_name

    def close(self) -> None:
        self.mmap_obj.close()
        self.file_obj.close()

    def __enter__(self) -> Tuple[mmap.mmap, str]:
        return self.mmap_obj, self.file_name

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()


class Manager(BaseManager):

    @safe_manager_call
    def init_manager(self) -> None:
        with self.namespace_lock:
            self.namespace.connected_processes = set()
            self.namespace.key = None
            self.namespace.service = None
            self.namespace.tags = {}

    @property
    @safe_manager_call
    def shared_memory_lock(self) -> AcquirerProxy:
        return self._get_shared_memory_lock()

    @property
    @safe_manager_call
    def namespace_lock(self) -> AcquirerProxy:
        return self._get_namespace_lock()

    @property
    @safe_manager_call
    def namespace(self) -> NamespaceProxy:
        return self._get_ns()

    @property
    @safe_manager_call
    def shared_memory_size(self) -> int:
        with self.namespace_lock:
            return self.namespace.shared_memory_size  # type: ignore[no-any-return]

    @shared_memory_size.setter
    @safe_manager_call
    def shared_memory_size(self, size: int) -> None:
        with self.namespace_lock:
            self.namespace.shared_memory_size = size

    @property
    @safe_manager_call
    def shared_memory_name(self) -> str:
        with self.namespace_lock:
            return self.namespace.shared_memory_name  # type: ignore[no-any-return]

    @shared_memory_name.setter
    @safe_manager_call
    def shared_memory_name(self, name: str) -> None:
        with self.namespace_lock:
            self.namespace.shared_memory_name = name

    @safe_manager_call
    def get_shared_memory(self) -> SharedMemoryContext:
        with self.shared_memory_lock, self.namespace_lock:
            if not hasattr(self.namespace, "shared_memory_size"):
                raise AttributeError(
                    "shared_memory_size must be set before shared_memory can be accessed"
                )
            if not hasattr(self.namespace, "shared_memory_name"):
                filename = os.path.join(
                    tempfile.gettempdir(), "hud_{}".format(uuid.uuid4())
                )
                with open(filename, "wb") as file:
                    file.truncate(self.namespace.shared_memory_size)
                    file.flush()
                self.namespace.shared_memory_name = filename
            else:
                filename = self.namespace.shared_memory_name
            shared_memory_file = open(filename, "r+b")  # type: BinaryIO
            mm = mmap.mmap(
                shared_memory_file.fileno(), self.namespace.shared_memory_size
            )
            return SharedMemoryContext(mm, shared_memory_file, filename)

    @property
    @safe_manager_call
    def connected_processes(self) -> Set[int]:
        return cast(Set[int], self.namespace.connected_processes)

    @connected_processes.setter
    @safe_manager_call
    def connected_processes(self, processes: Set[int]) -> None:
        with self.namespace_lock:
            self.namespace.connected_processes = processes

    @property
    @safe_manager_call
    def exporter_pid(self) -> int:
        if not hasattr(self, "_cached_exporter_pid"):
            with self.namespace_lock:
                self._cached_exporter_pid = cast(int, self.namespace.exporter_pid)
        return self._cached_exporter_pid

    @exporter_pid.setter
    @safe_manager_call
    def exporter_pid(self, pid: int) -> None:
        with self.namespace_lock:
            self.namespace.exporter_pid = pid

    @safe_manager_call
    def register_process(self, pid: int) -> None:
        with self.namespace_lock:
            processes = self.namespace.connected_processes
            processes.add(pid)
            self.namespace.connected_processes = processes

    @safe_manager_call
    def deregister_process(self, pid: int) -> None:
        with self.namespace_lock:
            processes = self.namespace.connected_processes
            processes.discard(pid)
            self.namespace.connected_processes = processes

    @safe_manager_call
    def register_service(self, key: str, service: str, tags: Dict[str, str]) -> None:
        with self.namespace_lock:
            self.namespace.key = key
            self.namespace.service = service
            self.namespace.tags = tags
        self.service_registered.set()

    @safe_manager_call
    def get_service(self) -> Tuple[str, str, Dict[str, str]]:
        with self.namespace_lock:
            return self.namespace.key, self.namespace.service, self.namespace.tags

    @property
    @safe_manager_call
    def manager_pid(self) -> int:
        if not hasattr(self, "_cached_manager_pid"):
            with self.namespace_lock:
                if not hasattr(self, "_cached_manager_pid"):
                    self._cached_manager_pid = cast(
                        int, self._get_manager_pid()._getvalue()
                    )
        return self._cached_manager_pid

    @property
    @safe_manager_call
    def session_id(self) -> Optional[str]:
        with self.namespace_lock:
            if not hasattr(self.namespace, "session_id"):
                return None
            return self.namespace.session_id  # type: ignore[no-any-return]

    @session_id.setter
    @safe_manager_call
    def session_id(self, session_id: str) -> None:
        with self.namespace_lock:
            self.namespace.session_id = session_id

    @property
    @safe_manager_call
    def fully_initialized(self) -> EventProxy:
        return self._get_fully_initialized_event()

    @property
    @safe_manager_call
    def service_registered(self) -> EventProxy:
        return self._get_service_registered_event()

    def _get_shared_memory_lock(self) -> AcquirerProxy:
        return NotImplemented

    def _get_namespace_lock(self) -> AcquirerProxy:
        return NotImplemented

    def _get_ns(self) -> NamespaceProxy:
        return NotImplemented

    def _get_manager_pid(self) -> BaseProxy:
        return NotImplemented

    def _get_fully_initialized_event(self) -> EventProxy:
        return NotImplemented

    def _get_service_registered_event(self) -> EventProxy:
        return NotImplemented


def get_manager(address: Any = None, authkey: Any = None) -> Manager:
    return Manager(address, authkey, ctx=multiprocessing.get_context("spawn"))
