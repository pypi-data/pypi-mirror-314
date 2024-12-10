import os
import platform
from typing import Optional

from ..logging import internal_logger
from ..schemas.events import KubernetesWorkloadData


def get_cpu_limit() -> Optional[str]:
    try:
        cpu_quota = read_file_safe("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
        cpu_period = read_file_safe("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
        if cpu_quota:
            if cpu_quota == "-1":
                return "unlimited"
            if not cpu_period:
                return None
            try:
                return str(int(cpu_quota) / int(cpu_period))
            except Exception as err:
                internal_logger.debug(
                    "Failed to calculate CPU limit with error: {}".format(err)
                )
                return None
        # cgroup v2
        cpu_max = read_file_safe("/sys/fs/cgroup/cpu.max")
        if not cpu_max:
            return None
        _max, period = cpu_max.split(" ")
        if _max == "max":
            return "unlimited"
        return str(float(_max) / float(period))
    except Exception as err:
        internal_logger.debug("Failed to get CPU limit with error: {}".format(err))
        return None


def get_memory_limit() -> Optional[str]:
    try:
        pod_memory_str = read_file_safe("/sys/fs/cgroup/memory/memory.stat")
        if not pod_memory_str:
            return None
        for line in pod_memory_str.split("\n"):
            if "hierarchical_memory_limit" in line:
                return line.split(" ")[1]
        return None
    except Exception as err:
        internal_logger.debug("Failed to get memory limit with error: {}".format(err))
        return None


def read_file_safe(file_path: str) -> Optional[str]:
    try:
        if not os.path.exists(file_path):
            internal_logger.debug("File {} not found".format(file_path))
            return None
        with open(
            file_path,
            "r",
            opener=lambda file, flags: os.open(file, flags | os.O_NONBLOCK),
        ) as file:
            return file.read()
    except FileNotFoundError:
        internal_logger.debug("File {} not found".format(file_path))
        return None
    except Exception as err:
        internal_logger.debug(
            "Failed to read file {} with error: {}".format(file_path, err)
        )
        return None


def is_running_in_docker() -> bool:
    # Check for the existence of the .dockerenv file
    return os.path.exists("/.dockerenv")


def get_kubernetes_workload_data(
    pod_cpu_limit: Optional[str] = None,
) -> Optional[KubernetesWorkloadData]:
    if platform.system() != "Linux":
        internal_logger.info(
            "Kubernetes workload data is only available on Linux",
            data=dict(os=platform.system()),
        )
        return None
    if not is_running_in_docker():
        internal_logger.info(
            "Not running in a container, skipping Kubernetes workload data"
        )
        return None
    hostname = platform.node()
    namespace = read_file_safe(
        "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    )
    product_uuid = read_file_safe("/sys/class/dmi/id/product_uuid")
    memory = get_memory_limit()
    return KubernetesWorkloadData(
        pod_name=hostname,
        pod_cpu_limit=str(pod_cpu_limit),
        pod_memory_limit=memory,
        pod_namespace=namespace,
        product_uuid=product_uuid,
    )
