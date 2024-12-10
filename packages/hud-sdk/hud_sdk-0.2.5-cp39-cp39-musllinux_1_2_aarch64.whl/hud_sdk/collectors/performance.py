import gc
import os

# import resource
import platform
import threading
import time
from typing import Dict, List, Optional, Tuple

from ..schemas.events import CpuData, Performance


class PerformanceMonitor:
    def __init__(self, owner: str, pod_cpu_limit: Optional[str] = None) -> None:
        self.owner = owner
        self.last_user_time, self.last_system_time = self._get_cpu_time()
        self.last_real_time = time.time()

        self.pod_cpu_limit = (
            float(pod_cpu_limit)
            if pod_cpu_limit and pod_cpu_limit != "unlimited"
            else None
        )

    @staticmethod
    def _get_cpu_time() -> Tuple[float, float]:
        user_time, system_time = os.times()[:2]
        return user_time, system_time

    def calculate_cpu_percentage(self) -> CpuData:
        # Get current CPU and real time
        user_time, system_time = self._get_cpu_time()
        real_time = time.time()

        if (
            self.last_user_time is not None
            and self.last_system_time is not None
            and self.last_real_time is not None
        ):
            cpu_time_delta = (user_time - self.last_user_time) + (
                system_time - self.last_system_time
            )
            real_time_delta = real_time - self.last_real_time
            cpu_percentage = (cpu_time_delta / real_time_delta) * 100

        # saved for next interation
        self.last_user_time, self.last_system_time, self.last_real_time = (
            user_time,
            system_time,
            real_time,
        )

        limited_cpu = None
        if self.pod_cpu_limit:
            limited_cpu = cpu_percentage / self.pod_cpu_limit

        return CpuData(
            user_time=user_time,
            system_time=system_time,
            elapsed_time=real_time,
            cpu_percentage=cpu_percentage,
            limited_cpu=limited_cpu,
        )

    @staticmethod
    def get_memory_usage() -> Optional[int]:
        current_platform = platform.system()

        if current_platform == "Linux":
            with open("/proc/self/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        return int(line.split()[1])
        return None

    @staticmethod
    def get_thread_count() -> int:
        return threading.active_count()

    @staticmethod
    def get_gc_stats() -> List[Dict[str, int]]:
        return gc.get_stats()

    def monitor_process(self) -> Performance:
        cpu = self.calculate_cpu_percentage()
        memory_usage = self.get_memory_usage()
        thread_count = self.get_thread_count()
        gc_stats = self.get_gc_stats()

        return Performance(
            cpu=cpu,
            max_rss=memory_usage,
            thread_count=thread_count,
            gc_stats=gc_stats,
            owner=self.owner,
        )
