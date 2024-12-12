from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from ..format_utils import format_path
from ..process_utils import get_current_pid
from .schema import JSON, Schema

CallersType = Tuple[Optional[Tuple[str, str, int, bool]], ...]


class Event(Schema):
    @classmethod
    def get_version(cls) -> str:
        return NotImplemented

    @classmethod
    def get_type(cls) -> str:
        return cls.__name__


class EventWithPid(Event):
    def to_json_data(self) -> Dict[JSON, JSON]:
        data = super().to_json_data()
        if "pid" not in data:
            data["pid"] = get_current_pid()
        return data


class ArgumentType(Enum):
    POSITIONAL_ONLY = "positional_only"
    ARG = "arg"
    VARARG = "vararg"
    KEYWORD_ONLY = "keyword_only"
    KWARG = "kwarg"


class FunctionArgument(Schema):
    def __init__(self, name: str, _type: ArgumentType):
        self.name = name
        self.type = _type


class CodeBlockType(Enum):
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"


class ScopeType(Enum):
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"


class ScopeNode(Schema):
    def __init__(self, type: ScopeType, name: str):
        self.type = type
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ScopeNode):
            return False
        return self.type == other.type and self.name == other.name


class FunctionDeclaration(Event):
    def __init__(
        self,
        file: str,
        function_id: str,
        is_async: bool,
        name: str,
        source_code_hash: str,
        start_line: int,
        end_line: Optional[int],
        code_block_type: CodeBlockType,
        arguments: Optional[List[FunctionArgument]] = None,
        scope: Optional[List[ScopeNode]] = None,
    ):
        self.file = file
        self.function_id = function_id
        self.is_async = is_async
        self.name = name
        self.source_code_hash = source_code_hash
        self.start_line = start_line
        self.end_line = end_line
        self.code_block_type = code_block_type
        self.arguments = arguments or []
        self.scope = scope or []

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class Caller(Schema):
    def __init__(self, name: str, file_name: str, start_line: int, is_wrapped: bool):
        self.name = name
        self.file_name = file_name
        self.start_line = start_line
        self.is_wrapped = is_wrapped


class Sketch(Schema):
    def __init__(self, bin_width: float, index_shift: int, data: List[int]):
        self.bin_width = bin_width
        self.index_shift = index_shift
        self.data = data


class Invocations(EventWithPid):
    def __init__(
        self,
        count: int,
        function_id: str,
        sampled_count: int,
        sum_duration: int,
        sum_squared_duration: int,
        timeslice: int,
        timestamp: datetime,
        callers: List[Caller],
        exceptions: Dict[str, int],
        sketch: Sketch,
        wrapped_flow_id: Optional[str],
        is_linked_function: bool,
    ):
        self.count = count
        self.function_id = function_id
        self.sampled_count = sampled_count
        self.sum_duration = sum_duration
        self.sum_squared_duration = sum_squared_duration
        self.timeslice = timeslice
        self.timestamp = timestamp
        self.callers = callers
        self.exceptions = exceptions
        self.sketch = sketch
        self.wrapped_flow_id = wrapped_flow_id
        self.is_linked_function = is_linked_function

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class AwsWorkloadData(Schema):
    def __init__(
        self,
        ami_id: str,
        launched_date: str,
        life_cycle: str,
        region: str,
        workload_id: str,
        workload_instance_type: str,
    ):
        self.ami_id = ami_id
        self.launched_date = launched_date
        self.life_cycle = life_cycle
        self.region = region
        self.workload_id = workload_id
        self.workload_instance_type = workload_instance_type


class KubernetesWorkloadData(Schema):
    def __init__(
        self,
        pod_name: str,
        pod_cpu_limit: Optional[str],
        pod_memory_limit: Optional[str],
        pod_namespace: Optional[str],
        product_uuid: Optional[str],
    ):
        self.pod_name = pod_name
        self.pod_cpu_limit = pod_cpu_limit
        self.pod_memory_limit = pod_memory_limit
        self.pod_namespace = pod_namespace
        self.product_uuid = product_uuid


class WorkloadData(Event):
    def __init__(
        self,
        aws_workload_data: Optional[AwsWorkloadData] = None,
        kubernetes_workload_data: Optional[KubernetesWorkloadData] = None,
    ):
        self.aws_workload_data = aws_workload_data
        self.kubernetes_workload_data = kubernetes_workload_data

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class ExceptionInfo(Schema):
    def __init__(self, name: str, value: str, stack_trace: str):
        self.name = name
        self.value = value
        self.stack_trace = stack_trace


class Log(EventWithPid):
    def __init__(
        self,
        message: str,
        data: Dict[str, Any],
        timestamp: float,
        level: str,
        pathname: str,
        lineno: int,
        exception: Optional[ExceptionInfo] = None,
    ):
        self.message = message
        self.data = data
        self.timestamp = timestamp
        self.level = level
        self.pathname = pathname
        self.lineno = lineno
        self.exc = exception

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class CpuData(Schema):
    def __init__(
        self,
        user_time: float,
        system_time: float,
        elapsed_time: float,
        cpu_percentage: float,
        limited_cpu: Optional[float] = None,
    ):
        self.user_time = user_time
        self.system_time = system_time
        self.elapsed_time = elapsed_time
        self.cpu_percentage = cpu_percentage
        self.limited_cpu = limited_cpu


class Performance(EventWithPid):
    def __init__(
        self,
        cpu: CpuData,
        max_rss: Optional[int],
        thread_count: int,
        gc_stats: List[Dict[str, int]],
        owner: str,
    ):
        self.cpu = cpu
        self.max_rss = max_rss
        self.thread_count = thread_count
        self.gc_stats = gc_stats
        self.owner = owner

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class Runtime(Event):
    def __init__(
        self,
        python_version: str,
        platform_info: str,
        architecture: str,
        pid: int,
        cwd: str,
        exec_path: str,
        argv: List[str],
    ):
        self.python_version = python_version
        self.platform_info = platform_info
        self.architecture = architecture
        self.pid = pid
        self.cwd = cwd
        self.exec_path = exec_path
        self.argv = argv

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class ModuleData(Schema):
    def __init__(self, name: str, version: Optional[str]):
        self.name = name
        self.version = version


class LoadedModules(EventWithPid):
    def __init__(self, modules: List[ModuleData]):
        self.modules = modules

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class InstalledPackages(Event):
    def __init__(self, modules: List[ModuleData]):
        self.modules = modules

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class EndpointDeclaration(Event):
    def __init__(self, flow_id: str, path: str, methods: List[str], framework: str):
        self.flow_id = flow_id
        self.path = format_path(path)
        self.methods = methods
        self.framework = framework

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class FlowMetric(EventWithPid):
    def __init__(
        self,
        flow_id: str,
        count: int,
        sum_duration: int,
        sum_squared_duration: int,
        timeslice: int,
        timestamp: datetime,
        sketch: Sketch,
    ):
        self.flow_id = flow_id
        self.count = count
        self.sum_duration = sum_duration
        self.sum_squared_duration = sum_squared_duration
        self.timeslice = timeslice
        self.timestamp = timestamp
        self.sketch = sketch

    @classmethod
    def get_version(cls) -> str:
        return "1.0.0"


class EndpointMetric(FlowMetric):
    def __init__(
        self,
        flow_id: str,
        count: int,
        sum_duration: int,
        sum_squared_duration: int,
        timeslice: int,
        timestamp: datetime,
        sketch: Sketch,
        status_code: int,
        route: str,
        method: str,
    ):
        super().__init__(
            flow_id,
            count,
            sum_duration,
            sum_squared_duration,
            timeslice,
            timestamp,
            sketch,
        )
        self.status_code = status_code
        self.route = route
        self.method = method
