import json
import traceback
from datetime import datetime
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

from .events import Log
from .schema import JSON, Schema


class Init(Schema):
    def __init__(
        self,
        sdk_version: str,
        service: str,
        start_time: datetime,
        token: str,
        type: str,
        tags: Dict[str, str],
    ):
        self.sdk_version = sdk_version
        self.service = service
        self.start_time = start_time
        self.token = token
        self.type = type
        self.version = "1.0.0"
        self.tags = tags


class Send(Schema):
    def __init__(
        self,
        event_version: str,
        raw: Any,
        send_time: datetime,
        source: str,
        type: str,
    ):
        self.event_version = event_version
        self.raw = raw
        self.send_time = send_time
        self.source = source
        self.type = type
        self.version = "1.0.0"


class Batch(Schema):
    def __init__(
        self,
        arr: List[Any],
        event_version: str,
        send_time: datetime,
        source: str,
        type: str,
    ):
        self.arr = arr
        self.event_version = event_version
        self.send_time = send_time
        self.source = source
        self.type = type
        self.version = "1.0.0"


class Logs(Schema):
    def __init__(
        self,
        logs: List[Log],
        send_time: datetime,
    ):
        self.logs = logs
        self.send_time = send_time

    def to_json_data(self) -> Dict[JSON, JSON]:
        logs = []  # type: List[str]
        for log in self.logs:
            try:
                logs.append(json.dumps(log.to_json_data()))
            except Exception:
                logs.append(
                    json.dumps(
                        Log(
                            "Failed to serialize log",
                            {
                                "exception": traceback.format_exc(),
                                "original_message": log.message,
                            },
                            log.timestamp,
                            "ERROR",
                            log.pathname,
                            log.lineno,
                        ).to_json_data()
                    )
                )
        return {
            "logs": "\n".join(logs),
            "send_time": self.send_time.isoformat(),
        }


class SessionlessLogs(Schema):
    def __init__(
        self,
        logs_request: Logs,
        token: str,
        service: str,
        sdk_version: str,
    ):
        self.logs_request = logs_request
        self.token = token
        self.service = service
        self.sdk_version = sdk_version

    def to_json_data(self) -> Dict[JSON, JSON]:
        return {
            **self.logs_request.to_json_data(),
            "token": self.token,
            "service": self.service,
            "sdk_version": self.sdk_version,
        }


class FatalError(Schema):

    class FatalErrorData:
        def __init__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            exc_traceback: Optional[TracebackType],
            pid: int,
            extra_message: Optional[str] = None,
        ):
            self.error_message = str(exc_value) if exc_value else ""
            self.error_name = exc_type.__name__ if exc_type else ""
            self.error_stack = (
                "".join(traceback.format_tb(exc_traceback)) if exc_traceback else ""
            )
            self.pid = pid
            self.extra_message = extra_message

    def __init__(
        self,
        fatal_error: FatalErrorData,
        send_time: datetime,
        token: Optional[str] = None,
        service: Optional[str] = None,
    ):
        self.error_message = fatal_error.error_message
        self.error_name = fatal_error.error_name
        self.error_stack = fatal_error.error_stack
        self.pid = fatal_error.pid
        self.extra_message = fatal_error.extra_message
        self.send_time = send_time
        self.token = token
        self.service = service
