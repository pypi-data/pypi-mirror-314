import asyncio
import contextlib
import json
import os
import signal
import time
from typing import TYPE_CHECKING, Any, Dict, Optional, Set, Union  # noqa: F401

import psutil  # noqa: F401

from ..client import (
    AsyncHandlerReturnType,  # noqa: F401
    Client,  # noqa: F401
    HudClientException,
    SyncHandlerReturnType,  # noqa: F401
    get_client,
)  # noqa: F401
from ..collectors.modules import get_installed_packages
from ..collectors.performance import PerformanceMonitor
from ..collectors.runtime import runtime_info
from ..config import config
from ..logging import internal_logger, send_logs_handler
from ..native import get_hud_running_mode
from ..process_utils import is_alive
from ..schemas import events
from ..schemas.events import WorkloadData
from ..user_options import init_user_options
from ..utils import suppress_exceptions_async, suppress_exceptions_sync
from ..workload_metadata import get_cpu_limit, get_workload_metadata
from .manager.server import Manager, get_manager  # noqa: F401
from .queue import BaseInfoStructure, BufferBackedCyclicQueue
from .task_manager import TaskManager

if TYPE_CHECKING:
    import mmap  # noqa: F401

    from .manager.manager import AcquirerProxy


class Exporter:
    def __init__(
        self,
        shared_memory_size: int = config.exporter_shared_memory_size,
    ):
        self.shared_memory_size = shared_memory_size
        self.client = (
            None
        )  # type: Optional[Client[AsyncHandlerReturnType] | Client[SyncHandlerReturnType]]

        # The task manager must be initialized using the currently running event loop, so we initialize it in the run method
        self.task_manager = None  # type: Optional[TaskManager]
        self.pod_cpu_limit = get_cpu_limit()
        self.perf_monitor = PerformanceMonitor("exporter", self.pod_cpu_limit)
        self.manager = None  # type: Optional[Manager]
        self._memory = None  # type: Optional[mmap.mmap]
        self._queue = None  # type: Optional[BufferBackedCyclicQueue[BaseInfoStructure]]
        self._queue_corrupt = False
        self.shared_memory_name = None  # type: Optional[str]
        self._connected_processes = set()  # type: Set[int]
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(exception_handler)
        loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self.handle_exit())
        )
        loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.handle_exit())
        )

    async def handle_exit(self) -> None:
        internal_logger.info("Received termination signal, stopping exporter")
        self.stop_tasks()

    async def send_event(self, event: events.Event) -> None:
        if self.client:
            if self.client.is_async:
                await self.client.send_event(event)
            else:
                self.client.send_event(event)

    async def send_json(self, data: Any, request_type: str) -> None:
        if self.client:
            handler = self.client.handler_from_json(data, request_type)
            if self.client.is_async:
                await handler(data, request_type)
            else:
                handler(data, request_type)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _log_runtime(self) -> None:
        runtime = runtime_info()
        internal_logger.info("Exporter Runtime data", data=runtime.to_json_data())

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_installed_packages(self) -> None:
        await self.send_event(get_installed_packages())

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_workload_data(self, workload_metadata: WorkloadData) -> None:
        await self.send_event(workload_metadata)

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _process_housekeeping(self) -> None:
        if not self.manager:
            return

        current_connected_processes = self.manager.connected_processes.copy()
        if current_connected_processes != self._connected_processes:
            self._connected_processes = current_connected_processes
            internal_logger.info(
                "Connected processes updated",
                data={"connected_processes": current_connected_processes},
            )

        if self.manager and not current_connected_processes:
            internal_logger.info("No connected processes, Shutting down")
            self.stop_tasks()
        elif self.manager:
            for process in current_connected_processes:
                if not is_alive(process):
                    internal_logger.info(
                        "Process {} has exited, Deregistering".format(process)
                    )
                    self.manager.deregister_process(process)

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _check_manager_lock(self) -> None:
        if self.manager:
            self._check_lock(self.manager.shared_memory_lock, "Manager lock")
            self._check_lock(self.manager.namespace_lock, "Namespace lock")

    def _check_lock(self, lock: "AcquirerProxy", lock_name: str) -> None:
        owner_info = lock.get_owner_and_locktime()
        if not owner_info:
            return
        owner, lock_time = owner_info
        current_time = time.time()
        elapsed_time = current_time - lock_time

        if isinstance(owner, int):
            internal_logger.critical(
                "Lock has been held by local thread , without process info",
                data={"lock_name": lock_name, "lock_time": lock_time},
            )
            self.stop_tasks()
        elif not is_alive(owner[0]):
            internal_logger.critical(
                "Lock has been held by process which has exited",
                data={"lock_name": lock_name, "owner": owner[0]},
            )
            self.stop_tasks()
        elif elapsed_time > config.manager_lock_critical_threshold:
            internal_logger.critical(
                "Lock has been held by process longer than critical threshold",
                data={
                    "lock_name": lock_name,
                    "owner": owner[0],
                    "critical_threshold": config.manager_lock_critical_threshold,
                },
            )
            self.stop_tasks()
        elif elapsed_time > config.manager_lock_warning_threshold:
            internal_logger.warning(
                "Lock has been held by process longer than warning threshold",
                data={
                    "lock_name": lock_name,
                    "owner": owner[0],
                    "warning_threshold": config.manager_lock_warning_threshold,
                },
            )

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _check_queue_utilization(self) -> None:
        if not self._queue:
            return
        buffer_size = self._queue.get_buffer_size()
        utilization = (
            (buffer_size - await self._queue.async_get_available()) / buffer_size
        ) * 100
        if utilization > config.shared_memory_utilization_warning_threshold:
            internal_logger.warning(
                "Queue utilization is at {:.2f}%".format(utilization)
            )

        if utilization > config.shared_memory_utilization_critical_threshold:
            internal_logger.critical(
                "Queue utilization is at {:.2f}%".format(utilization)
            )

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _check_exporter_disabled(self) -> None:
        if not get_hud_running_mode():
            internal_logger.critical("HUD is disabled, stopping exporter")
            self.stop_tasks()

    @suppress_exceptions_async(default_return_factory=lambda: False)
    async def queue_processor(self) -> bool:
        if not self.task_manager:
            return False
        if not self._queue:
            return False
        if self._queue_corrupt:
            return False
        next = await self._queue.async_popleft()
        if next is not None:
            try:
                data, request_type = json.loads(next)
            except Exception:
                internal_logger.exception(
                    "Failed to load data from queue. Queue state may be corrupted"
                )
                self._queue_corrupt = True
                self.stop_tasks()
                return False
            self.task_manager.register_task(self.send_json, data, request_type)
            return True
        return False

    async def process_queue_until_empty(self) -> None:
        while await self.queue_processor():
            pass

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _check_manager(self) -> None:
        if self.manager:
            pid = self.manager.manager_pid
            if not is_alive(pid):
                internal_logger.critical("Manager process has exited")
                self.stop_tasks()
        else:
            internal_logger.critical("Manager process hasn't been properly initialized")
            self.stop_tasks()

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _dump_logs(self) -> None:
        logs = send_logs_handler.get_and_clear_logs()
        if logs:
            await self.send_json(logs.to_json_data(), "Logs")

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_performance(self) -> None:
        performance = self.perf_monitor.monitor_process()
        if config.log_performance:
            internal_logger.info("performance data", data=performance.to_json_data())
        if self.client:
            await self.client.send_event(performance)

    def stop_tasks(self) -> None:
        if self.task_manager:
            self.task_manager.stop_running_tasks()

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _check_existence_of_multiple_exporters(self) -> None:
        for ps in psutil.process_iter():
            try:
                if "hud_sdk.exporter" in ps.cmdline() and ps.pid != os.getpid():
                    internal_logger.warning(
                        "Multiple exporters detected. Another exporter found with PID: {}".format(
                            ps.pid
                        )
                    )
            except (psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
                pass

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _initialize_workload_metadata(self) -> None:
        workload_metadata = await get_workload_metadata(self.pod_cpu_limit)
        await self._send_workload_data(workload_metadata)
        if self.task_manager:
            self.task_manager.register_periodic_task(
                self._send_workload_data,
                config.workload_data_flush_interval,
                workload_metadata,
            )

    async def cleanup(self) -> None:
        internal_logger.info("Cleaning up exporter")
        if self._memory:
            with contextlib.suppress(Exception):
                self._memory.close()
            try:
                if self.shared_memory_name:
                    os.remove(self.shared_memory_name)
                    internal_logger.info(
                        "Removed shared memory file",
                        data={"file": self.shared_memory_name},
                    )
            except Exception:
                internal_logger.exception(
                    "Failed to remove shared memory file",
                    data={"file": self.shared_memory_name},
                )

            self._memory = None

        await self._dump_logs()
        # Logs after this point will not be sent to the server

        if self.client:
            if self.client.is_async:
                await self.client.close()
            else:
                self.client.close()
            self.client = None

        if self.manager:
            with contextlib.suppress(Exception):
                self.manager.shutdown()
            self.manager = None

    async def run(self) -> None:
        with contextlib.ExitStack() as stack:
            manager = stack.enter_context(
                get_manager(("localhost", 0), config.manager_password)
            )

            # Used to communicate port with parent process. TODO: Use a better method
            print(manager.address[1], flush=True)

            if config.testing_output_directory:
                with open(
                    os.path.join(config.testing_output_directory, "exporter_pid.txt"),
                    "w",
                ) as f:
                    print(os.getpid(), file=f)

                with open(
                    os.path.join(
                        config.testing_output_directory, "exporter_pid_written"
                    ),
                    "w",
                ) as f:
                    pass

            self.manager = manager
            manager.init_manager()
            manager.exporter_pid = os.getpid()
            manager.shared_memory_size = self.shared_memory_size

            self._memory, self.shared_memory_name = stack.enter_context(
                manager.get_shared_memory()
            )

            # The queue must only be accessed as long as the shared memory is available
            self._queue = BufferBackedCyclicQueue(
                self._memory,
                BaseInfoStructure,
                manager.shared_memory_lock,
                self._memory.size(),
            )
            if not self.manager.service_registered.wait(
                timeout=config.exporter_service_registered_timeout
            ):
                internal_logger.critical("Manager did not register service")
                await self.cleanup()
                return
            init_user_options(*self.manager.get_service(), False)

            try:
                self.client = get_client(is_async=True)
                if self.client.is_async:
                    await self.client.init_session()
                else:
                    self.client.init_session()
            except Exception as e:
                await self.cleanup()
                if not isinstance(e, HudClientException):
                    internal_logger.exception("Failed to initialize client")
                return

            if self.client.session_id:
                manager.session_id = self.client.session_id
            else:
                internal_logger.warning("Client did not return a session id")

            manager.fully_initialized.set()
            internal_logger.info("Manager process fully initialized")

            self.task_manager = TaskManager()

            self.task_manager.register_periodic_task(
                self._check_manager, config.exporter_manager_check_interval
            )
            self.task_manager.register_periodic_task(
                self.queue_processor,
                config.exporter_queue_process_interval,
                callback=self.process_queue_until_empty,
            )

            self._check_existence_of_multiple_exporters()

            loop = asyncio.get_event_loop()
            task_manager = self.task_manager
            loop.call_later(
                config.exporter_process_registry_warmup_period,
                lambda: task_manager.register_periodic_task(
                    self._process_housekeeping,
                    config.exporter_process_registry_update_interval,
                ),
            )

            self.task_manager.register_task(self._initialize_workload_metadata)
            self.task_manager.register_task(
                self._log_runtime
            )  # We don't need to send runtime info periodically
            self.task_manager.register_task(
                self._send_installed_packages
            )  # We don't need to send installed packages periodically
            self.task_manager.register_periodic_task(
                self._check_manager_lock, config.manager_lock_owner_check_interval
            )
            self.task_manager.register_periodic_task(
                self._check_queue_utilization,
                config.shared_memory_utilization_check_interval,
            )
            self.task_manager.register_periodic_task(
                self._check_exporter_disabled, config.exporter_disabled_check_interval
            )
            self.task_manager.register_periodic_task(
                self._dump_logs, config.logs_flush_interval
            )
            self.task_manager.register_periodic_task(
                self._send_performance, config.performace_report_interval
            )
            try:
                await self.task_manager.wait_for_tasks()
                internal_logger.info("Loop has exited gracefully")
            except Exception:
                internal_logger.exception("Exception in worker loop")
            finally:
                try:
                    await self.cleanup()
                except Exception:
                    pass


def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    internal_logger.error(
        "Exception in exporter loop", data={"message": context["message"]}
    )
