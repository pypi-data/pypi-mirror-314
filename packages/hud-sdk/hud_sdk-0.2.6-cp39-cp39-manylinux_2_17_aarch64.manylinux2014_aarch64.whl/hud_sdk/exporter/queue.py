import asyncio
import ctypes
import mmap
import struct
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Generic,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

if TYPE_CHECKING:
    from typing import Protocol, Self

    class Lockable(Protocol):
        def acquire(self, blocking: bool = True, timeout: int = -1) -> bool: ...
        async def async_acquire(
            self, blocking: bool = True, timeout: int = -1
        ) -> bool: ...

        def release(self) -> None: ...
        async def async_release(self) -> None: ...

        def __enter__(self) -> bool: ...
        async def __aenter__(self) -> bool: ...

        def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
        async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
        def get_owner_and_locktime(
            self,
        ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]: ...

else:
    Lockable = Any


class BaseInfoStructure(ctypes.Structure):
    head = 0  # type: int
    tail = 0  # type: int
    available = 0  # type: int
    _fields_ = [
        ("head", ctypes.c_uint32),
        ("tail", ctypes.c_uint32),
        ("available", ctypes.c_uint32),
    ]


InfoStructType = TypeVar("InfoStructType", bound=BaseInfoStructure)
T = TypeVar("T")


class CyclicBufferView:
    def __init__(self, buffer: mmap.mmap, buffer_size: int):
        self.buffer_size = buffer_size
        self.buffer = buffer

    @overload
    def __getitem__(self, key: int) -> int: ...
    @overload
    def __getitem__(self, key: slice) -> bytes: ...

    def __getitem__(self, key: Union[slice, int]) -> Union[bytes, int]:
        if isinstance(key, int):
            if key > 0:
                key = key % self.buffer_size
            return self.buffer[key]
        length = key.stop - key.start
        if self.buffer_size - key.start < length:
            return bytes(self.buffer[key.start : self.buffer_size]) + bytes(
                self.buffer[: length - (self.buffer_size - key.start)]
            )
        else:
            return bytes(self.buffer[key])

    def __setitem__(self, key: slice, value: bytes) -> None:
        if isinstance(key, int):
            if key > 0:
                key = key % self.buffer_size
            self.buffer[key] = value
            return
        length = key.stop - key.start
        if self.buffer_size - key.start < length:
            self.buffer[key.start : self.buffer_size] = value[
                : self.buffer_size - key.start
            ]
            self.buffer[: length - (self.buffer_size - key.start)] = value[
                self.buffer_size - key.start :
            ]
        else:
            self.buffer[key] = value


class ContextWrapper(Generic[T]):
    def __init__(self, wrapped: T):
        super().__setattr__("_wrapped", wrapped)

    def in_context(self) -> bool:
        return True

    # Override setattr and getattr to bind the wrapped object's descriptors (functions, properties) to the wrapper object.
    def __getattr__(self, name: str) -> Any:
        try:
            func = getattr(type(self._wrapped), name)
            return func.__get__(self, type(self._wrapped))
        except AttributeError:
            return getattr(self._wrapped, name)

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            func = getattr(type(self._wrapped), name)
            func.__set__(self, value)
        except AttributeError:
            setattr(self._wrapped, name, value)


class BufferBackedCyclicQueue(Generic[InfoStructType]):
    def __init__(
        self,
        buffer: mmap.mmap,
        info_struct_type: Type[InfoStructType],
        lock: Lockable,
        size: int,
    ):
        self._in_sync_context = False
        self.buffer = buffer
        self.info_struct_type = info_struct_type
        self.lock = lock
        self._timeout = 8
        self._buffer_size = size - ctypes.sizeof(info_struct_type)
        if self.available == 0:
            self.available = self._buffer_size

        self.buffer_view = CyclicBufferView(buffer, self._buffer_size)

    def in_context(self) -> bool:
        return False

    @overload
    def synchronized(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]: ...  # type: ignore[misc]
    @overload
    def synchronized(func: Callable[..., T]) -> Callable[..., T]: ...  # type: ignore[misc]
    def synchronized(func: Callable[..., T]) -> Union[Callable[..., T], Callable[..., Coroutine[Any, Any, T]]]:  # type: ignore[misc]
        if asyncio.iscoroutinefunction(func):

            async def synchronization_wrapper(
                self: "Self", *args: Any, **kwargs: Any
            ) -> T:
                if self.in_context():
                    return await func(self, *args, **kwargs)  # type: ignore[no-any-return]
                acquired_lock = False
                try:
                    if not await self.lock.async_acquire(timeout=self._timeout):
                        raise TimeoutError("Could not acquire lock")
                    acquired_lock = True
                    return await func(ContextWrapper(self), *args, **kwargs)  # type: ignore[no-any-return]
                finally:
                    if acquired_lock:
                        await self.lock.async_release()

        else:

            def synchronization_wrapper(self: "Self", *args: Any, **kwargs: Any) -> T:  # type: ignore[misc]
                if self.in_context():
                    return func(self, *args, **kwargs)
                acquired_lock = False
                try:
                    if not self.lock.acquire(timeout=self._timeout):
                        raise TimeoutError("Could not acquire lock")
                    acquired_lock = True
                    return func(ContextWrapper(self), *args, **kwargs)
                finally:
                    if acquired_lock:
                        self.lock.release()

        return synchronization_wrapper

    # This should only be used directly in a synchronized context
    @property
    @synchronized
    def _info(self) -> InfoStructType:
        return self.info_struct_type.from_buffer(self.buffer, self._buffer_size)

    def get_buffer_size(self) -> int:
        return self._buffer_size

    @property
    @synchronized
    def available(self) -> int:
        return self._info.available

    @available.setter
    @synchronized
    def available(self, value: int) -> None:
        self._info.available = value

    @synchronized
    async def async_get_available(self) -> int:
        return self._info.available

    @synchronized
    def push(self, data: bytes) -> bool:
        data_to_write = struct.pack("I", len(data)) + data
        if len(data_to_write) > self._info.available:
            return False

        address = self._info.tail
        self._info.available -= len(data_to_write)

        self.buffer_view[address : address + len(data_to_write)] = data_to_write

        self._info.tail = (address + len(data_to_write)) % self._buffer_size
        return True

    @synchronized
    def popleft(self) -> Optional[bytes]:
        if self._info.head == self._info.tail and self._info.available > 0:
            return None

        len_address = self._info.head
        data_address = len_address + 4
        length = struct.unpack(
            "I", bytearray(self.buffer_view[self._info.head : self._info.head + 4])
        )[0]
        data = self.buffer_view[data_address : data_address + length]
        self._info.head = (data_address + length) % self._buffer_size
        self._info.available += length + 4
        return data

    @synchronized
    async def async_popleft(self) -> Optional[bytes]:
        return self.popleft()

    del synchronized
