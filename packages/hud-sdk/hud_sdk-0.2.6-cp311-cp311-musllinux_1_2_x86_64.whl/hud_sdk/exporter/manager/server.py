__all__ = ["get_manager", "Manager"]

import os
import threading

from .manager import (
    AcquirerProxy,
    EventProxy,
    Manager,
    NamespaceProxy,
    OwnedLock,
    get_manager,
)

shared_memory_lock = OwnedLock()


def get_shared_memory_lock() -> OwnedLock:
    return shared_memory_lock


Manager.register(
    "_get_shared_memory_lock", callable=get_shared_memory_lock, proxytype=AcquirerProxy
)

namespace_lock = OwnedLock()


def get_namespace_lock() -> OwnedLock:
    return namespace_lock


Manager.register(
    "_get_namespace_lock", callable=get_namespace_lock, proxytype=AcquirerProxy
)


class Namespace:
    pass


ns = Namespace()


def get_ns() -> object:
    return ns


Manager.register("_get_ns", callable=get_ns, proxytype=NamespaceProxy)

Manager.register("_get_manager_pid", callable=os.getpid)


fully_initialized_event = threading.Event()


def _get_fully_initialized_event() -> threading.Event:
    return fully_initialized_event


Manager.register(
    "_get_fully_initialized_event",
    callable=_get_fully_initialized_event,
    proxytype=EventProxy,
)

service_registered_event = threading.Event()


def _get_service_registered_event() -> threading.Event:
    return service_registered_event


Manager.register(
    "_get_service_registered_event",
    callable=_get_service_registered_event,
    proxytype=EventProxy,
)
