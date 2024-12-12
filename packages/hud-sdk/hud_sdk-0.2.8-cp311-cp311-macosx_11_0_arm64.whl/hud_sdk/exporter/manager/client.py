__all__ = ["get_manager", "Manager"]

from .manager import AcquirerProxy, EventProxy, Manager, NamespaceProxy, get_manager

Manager.register("_get_shared_memory_lock", proxytype=AcquirerProxy)
Manager.register("_get_namespace_lock", proxytype=AcquirerProxy)
Manager.register("_get_ns", proxytype=NamespaceProxy)
Manager.register("_get_manager_pid")
Manager.register("_get_fully_initialized_event", proxytype=EventProxy)
Manager.register("_get_service_registered_event", proxytype=EventProxy)
