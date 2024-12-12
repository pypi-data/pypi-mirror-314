__all__ = [
    "ForksafeSequence",
    "ForksafeMapping",
    "ForksafeLock",
    "ForksafeWrapper",
    "ForksafeCM",
]

import os
import typing
from threading import Lock, RLock
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    MutableSequence,
    TypeVar,
)


class ForkCallbacks:
    def __init__(self) -> None:
        self.callbacks = []  # type: list[Callable[..., Any]]
        self.resources = []  # type: list[Callable[..., Any]]

    def register_callback(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.callbacks.append(func)
        return func

    def register_resource(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.resources.append(func)
        return func

    def register(self, func: Callable[..., Any]) -> Callable[..., Any]:
        raise NotImplementedError("Use register_callback or register_resource")

    def execute_all(self) -> None:
        try:
            for func in self.resources:
                func()
            for func in self.callbacks:
                func()
        except Exception:
            from .native import set_hud_running_mode
            from .utils import send_fatal_error

            # TODO: Try to use another identifier, or make key and service global.
            set_hud_running_mode(False)
            send_fatal_error(message="Failed to execute fork callbacks")


before_fork = ForkCallbacks()
after_fork_in_parent = ForkCallbacks()
after_fork_in_child = ForkCallbacks()

if hasattr(os, "register_at_fork"):
    os.register_at_fork(
        before=before_fork.execute_all,
        after_in_parent=after_fork_in_parent.execute_all,
        after_in_child=after_fork_in_child.execute_all,
    )

try:
    import uwsgi  # type: ignore[import-not-found]

    if getattr(uwsgi, "post_fork_hook", None):
        previous_uwsgi_fork_hook = uwsgi.post_fork_hook
        after_fork_in_child.register_callback(previous_uwsgi_fork_hook)
    uwsgi.post_fork_hook = after_fork_in_child.execute_all
except ImportError:
    pass


@before_fork.register_callback
def _before_fork() -> None:
    from .logging import internal_logger

    internal_logger.info("Process is about to fork")


T = TypeVar("T")
W = TypeVar("W")


class ForksafeWrapper(typing.Generic[T]):
    def __init__(self, factory: Callable[[], T]) -> None:
        self.factory = factory
        after_fork_in_child.register_resource(self.reset_wrapped)
        self.reset_wrapped()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.obj, name)

    def get_wrapped(self) -> T:
        return self.obj

    def reset_wrapped(self) -> None:
        self.obj = self.factory()


class ForksafeCM(ForksafeWrapper[ContextManager[T]]):
    def __enter__(self) -> T:
        return self.obj.__enter__()

    def __exit__(self, *args: Any) -> Any:
        return self.obj.__exit__(*args)


class ForksafeSequence(ForksafeWrapper[MutableSequence[T]]):
    def __len__(self) -> int:
        return len(self.obj)

    def __getitem__(self, key: Any) -> Any:
        return self.obj.__getitem__(key)

    def __setitem__(self, key: Any, value: T) -> None:
        self.obj.__setitem__(key, value)


class ForksafeMapping(ForksafeWrapper[Dict[T, W]]):
    def __len__(self) -> int:
        return len(self.obj)

    def __getitem__(self, key: T) -> W:
        return self.obj.__getitem__(key)

    def __setitem__(self, key: T, value: W) -> None:
        self.obj.__setitem__(key, value)


class ForksafeLock(ForksafeCM[bool]):
    def __init__(self) -> None:
        super().__init__(Lock)


class ForksafeRLock(ForksafeCM[bool]):
    def __init__(self) -> None:
        super().__init__(RLock)
