import asyncio
import json
import pprint
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Generic,
    List,
    Optional,  # noqa: F401
    Type,
    TypeVar,
    cast,
)

import aiohttp
import requests
from requests.adapters import HTTPAdapter, Retry

from .config import config
from .logging import internal_logger
from .schemas import events
from .schemas.requests import (
    Batch as BatchRequest,
)
from .schemas.requests import (
    FatalError as FatalErrorRequest,
)
from .schemas.requests import (
    Init as InitRequest,
)
from .schemas.requests import (
    Send as SendRequest,
)
from .user_options import get_user_options
from .version import version as hud_version


class HudClientException(Exception):
    pass


SyncHandlerReturnType = Any
AsyncHandlerReturnType = Coroutine[Any, Any, Any]
HandlerReturnType = TypeVar(
    "HandlerReturnType", AsyncHandlerReturnType, SyncHandlerReturnType
)


class Client(Generic[HandlerReturnType], ABC):
    session_id = None  # type: Optional[str]

    def set_session_id(self, session_id: str) -> None:
        internal_logger.info("Setting session_id", data=dict(session_id=session_id))
        self.session_id = session_id

    def handler_from_json(
        self, data: Any, request_type: str
    ) -> Callable[[Any, str], HandlerReturnType]:
        if request_type == "Logs":
            return self.send_logs_json
        elif isinstance(data, list):
            return self.send_batch_json
        elif isinstance(data, dict):
            return self.send_single_json
        else:
            raise HudClientException("Unknown request type: {}".format(request_type))

    @abstractmethod
    def init_session(self) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_event(self, event: events.Event) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_logs_json(self, data: Any, request_type: str) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_sessionless_logs_json(
        self, data: Any, request_type: str
    ) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_batch_json(self, data: Any, request_type: str) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_single_json(self, data: Any, request_type: str) -> HandlerReturnType:
        pass

    @abstractmethod
    def send_fatal_error(self, fatal_error: FatalErrorRequest.FatalErrorData) -> None:
        pass

    @abstractmethod
    def close(self) -> HandlerReturnType:
        pass

    @property
    @abstractmethod
    def is_async(self) -> bool:
        pass


class ConsoleClient(Client[SyncHandlerReturnType]):
    def init_session(self) -> None:
        print("init_session", file=sys.stderr)

    def send_logs_json(self, data: Any, request_type: str) -> None:
        print("send_logs_json", file=sys.stderr)
        for log in data["logs"]:
            pprint.pprint({"type": "Log", **log}, stream=sys.stderr, sort_dicts=False)

    def send_sessionless_logs_json(self, data: Any, request_type: str) -> None:
        print("send_sessionless_logs_json", file=sys.stderr)
        for log in data["logs"]:
            pprint.pprint({"type": "Log", **log}, stream=sys.stderr, sort_dicts=False)

    def send_batch_json(self, data: Any, request_type: str) -> None:
        print("Send batch of {} {}".format(len(data), request_type), file=sys.stderr)
        for item in data:
            pprint.pprint(
                {"type": request_type, **item}, stream=sys.stderr, sort_dicts=False
            )

    def send_single_json(self, data: Any, request_type: str) -> None:
        print("Send single {}".format(request_type), file=sys.stderr)
        pprint.pprint(
            {"type": request_type, **data}, stream=sys.stderr, sort_dicts=False
        )

    def send_event(self, event: events.Event) -> None:
        json_data = event.to_json_data()
        event_type = event.get_type()
        handler = self.handler_from_json(json_data, event_type)
        handler(json_data, event_type)

    @property
    def is_async(self) -> bool:
        return False

    def close(self) -> None:
        return

    def send_fatal_error(self, fatal_error: FatalErrorRequest.FatalErrorData) -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
        )
        print(
            "send_fatal_error: {}".format(fatal_error_request.to_json_data()),
            file=sys.stderr,
        )


class JSONClient(Client[SyncHandlerReturnType]):
    def __init__(self, path: str) -> None:
        self.path = path

    def _write_to_json(self, data: Any) -> None:
        with open(self.path, mode="a") as file:
            file.write(json.dumps(data) + "\n")

    def init_session(self) -> None:
        self._write_to_json({"type": "init_session"})

    def send_logs_json(self, data: Any, request_type: str) -> None:
        for log in data["logs"]:
            self._write_to_json({"type": "log", **log})

    def send_sessionless_logs_json(self, data: Any, request_type: str) -> None:
        for log in data["logs"]:
            self._write_to_json({"type": "log", **log})

    def send_batch_json(self, data: Any, request_type: str) -> None:
        for item in data:
            self._write_to_json({"type": request_type, **item})

    def send_single_json(self, data: Any, request_type: str) -> None:
        self._write_to_json({"type": request_type, **data})

    def send_event(self, event: events.Event) -> None:
        json_data = event.to_json_data()
        event_type = event.get_type()
        handler = self.handler_from_json(json_data, event_type)
        handler(json_data, event_type)

    @property
    def is_async(self) -> bool:
        return False

    def close(self) -> None:
        return

    def send_fatal_error(self, fatal_error: FatalErrorRequest.FatalErrorData) -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error, send_time=datetime.now(timezone.utc)
        )
        self._write_to_json(
            {"type": "fatal_error", **fatal_error_request.to_json_data()}
        )


class BaseHttpClient(Client[HandlerReturnType]):
    source = "python-sdk"

    def __init__(
        self, host: str, api_key: str, service: str, tags: Dict[str, str]
    ) -> None:
        self.host = host
        self.api_key = api_key
        self.service = service
        self.tags = tags
        self.session = None  # type: Optional[aiohttp.ClientSession | requests.Session]
        self.session_id = None  # type: Optional[str]
        self.max_retries = config.api_max_retries
        self.backoff_factor = config.api_backoff_factor
        self.status_forcelist = [429, 500, 502, 503, 504]

    @abstractmethod
    def _send(self, uri: str, request: Any, request_type: str) -> HandlerReturnType:
        pass

    def set_session_id(self, session_id: str) -> None:
        super().set_session_id(session_id)
        if self.session:
            self.session.headers["X-Session-ID"] = session_id


class AsyncHttpClient(BaseHttpClient[AsyncHandlerReturnType]):
    def __init__(
        self, host: str, api_key: str, service: str, tags: Dict[str, str]
    ) -> None:
        super().__init__(host, api_key, service, tags)
        self.session = aiohttp.ClientSession()  # type: aiohttp.ClientSession
        self.timeout = None  # type: Optional[aiohttp.ClientTimeout | float]
        if hasattr(aiohttp, "ClientTimeout"):
            self.timeout = aiohttp.ClientTimeout(total=config.api_timeout)
        else:
            self.timeout = config.api_timeout

    @property
    def is_async(self) -> bool:
        return True

    async def _send(self, uri: str, request: Any, request_type: str) -> Any:
        url = "{}/{}".format(self.host, uri)
        headers = {"Content-Type": "application/json"}

        if self.session_id:
            headers["X-Session-ID"] = self.session_id
        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    url,
                    data=json.dumps(request),
                    headers=headers,
                    timeout=self.timeout,  # type: ignore[arg-type]
                ) as res:
                    if (
                        res.status in self.status_forcelist
                        and attempt < self.max_retries - 1
                    ):
                        await asyncio.sleep(self.backoff_factor * (2**attempt))
                        continue
                    res.raise_for_status()
                    return await res.json()
            except Exception as e:
                if (
                    isinstance(e, asyncio.TimeoutError)
                    and attempt < self.max_retries - 1
                ):
                    await asyncio.sleep(self.backoff_factor * (2**attempt))
                    continue
                internal_logger.exception(
                    "Failed to send request", data=dict(type=request_type)
                )
                raise

    async def init_session(self) -> None:
        internal_logger.debug(
            "Initializing session for service", data=dict(service=self.service)
        )
        request = InitRequest(
            token=self.api_key,
            service=self.service,
            start_time=datetime.now(timezone.utc),
            type=self.source,
            sdk_version=hud_version,
            tags=self.tags,
        )
        internal_logger.info("Sending request", data={"type": "Init"})
        res = await self._send("sink/init", request.to_json_data(), "Init")
        session_id = res["sessionId"]
        self.set_session_id(session_id)

    async def send_logs_json(self, data: Any, request_type: str) -> None:
        await self._send("sink/logs", data, request_type)

    async def send_sessionless_logs_json(self, data: Any, request_type: str) -> None:
        internal_logger.info("Sending request", data={"type": request_type})
        await self._send("sink/sessionless-logs", data, request_type)

    async def send_batch_json(self, data: Any, request_type: str) -> None:
        arr = cast(List[Any], data)
        size = config.batch_size
        version = cast(Type[events.Event], getattr(events, request_type)).get_version()
        internal_logger.info("Sending request", data={"type": request_type})
        for i in range(0, len(arr), size):
            request = BatchRequest(
                arr=[i for i in arr[i : i + size]],
                event_version=version,
                send_time=datetime.now(timezone.utc),
                source=self.source,
                type=request_type,
            )
            await self._send("sink/batch", request.to_json_data(), request_type)

    async def send_single_json(self, data: Any, request_type: str) -> None:
        internal_logger.info("Sending request", data={"type": request_type})
        request = SendRequest(
            event_version=getattr(events, request_type).get_version(),
            send_time=datetime.now(timezone.utc),
            source=self.source,
            type=request_type,
            raw=data,
        )
        await self._send("sink/send", request.to_json_data(), request_type)

    async def send_event(self, event: events.Event) -> None:
        json_data = event.to_json_data()
        event_type = event.get_type()
        handler = self.handler_from_json(json_data, event_type)
        await handler(json_data, event_type)

    def send_fatal_error(self, fatal_error: FatalErrorRequest.FatalErrorData) -> None:
        raise NotImplementedError(
            "send_fatal_error is not implemented for async client"
        )

    async def close(self) -> None:
        await self.session.close()


class SyncHttpClient(BaseHttpClient[SyncHandlerReturnType]):
    def __init__(
        self, host: str, api_key: str, service: str, tags: Dict[str, str]
    ) -> None:
        super().__init__(host, api_key, service, tags)
        self.session = requests.Session()  # type: requests.Session
        self.session.mount(
            self.host,
            HTTPAdapter(
                max_retries=Retry(
                    total=config.api_max_retries,
                    backoff_factor=config.api_backoff_factor,
                    status_forcelist=self.status_forcelist,
                )
            ),
        )

    def _send(self, uri: str, request: Any, request_type: str) -> Any:
        try:
            with self.session.post(
                "{}/{}".format(self.host, uri),
                json=request,
            ) as res:
                res.raise_for_status()
                return res.json()
        except Exception:
            internal_logger.exception(
                "Failed to send request", data=dict(type=request_type)
            )
            raise

    @property
    def is_async(self) -> bool:
        return False

    def close(self) -> None:
        self.session.close()

    def init_session(self) -> None:
        internal_logger.info("Sending request", data={"type": "Init"})
        internal_logger.debug(
            "Initializing session for service", data=dict(service=self.service)
        )
        request = InitRequest(
            token=self.api_key,
            service=self.service,
            start_time=datetime.now(timezone.utc),
            type=self.source,
            sdk_version=hud_version,
            tags=self.tags,
        )
        res = self._send("sink/init", request.to_json_data(), "Init")
        session_id = res["sessionId"]
        self.set_session_id(session_id)

    def send_logs_json(self, data: Any, request_type: str) -> None:
        internal_logger.info("Sending request", data={"type": request_type})
        self._send("sink/logs", data, request_type)

    def send_sessionless_logs_json(self, data: Any, request_type: str) -> None:
        self._send("sink/sessionless-logs", data, request_type)

    def send_batch_json(self, data: Any, request_type: str) -> None:
        arr = cast(List[Any], data)
        size = config.batch_size
        version = cast(Type[events.Event], getattr(events, request_type)).get_version()
        internal_logger.info("Sending request", data={"type": request_type})
        for i in range(0, len(arr), size):
            request = BatchRequest(
                arr=[i for i in arr[i : i + size]],
                event_version=version,
                send_time=datetime.now(timezone.utc),
                source=self.source,
                type=request_type,
            )
            self._send("sink/batch", request.to_json_data(), request_type)

    def send_single_json(self, data: Any, request_type: str) -> None:
        internal_logger.info("Sending request", data={"type": request_type})
        request = SendRequest(
            event_version=getattr(events, request_type).get_version(),
            send_time=datetime.now(timezone.utc),
            source=self.source,
            type=request_type,
            raw=data,
        )
        self._send("sink/send", request.to_json_data(), request_type)

    def send_fatal_error(self, fatal_error: FatalErrorRequest.FatalErrorData) -> None:
        internal_logger.info("Sending request", data={"type": "FatalError"})
        request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
            token=self.api_key,
            service=self.service,
        )
        self._send("sink/redline", request.to_json_data(), "FatalError")

    def send_event(self, event: events.Event) -> None:
        json_data = event.to_json_data()
        event_type = event.get_type()
        handler = self.handler_from_json(json_data, event_type)
        handler(json_data, event_type)


def get_client(
    is_async: bool = False,
) -> Client[HandlerReturnType]:

    client_type = config.client_type
    if client_type == "console":
        return ConsoleClient()
    if client_type == "json":
        return JSONClient(config.json_path)
    if client_type == "http":
        host = config.host
        if not host:
            internal_logger.warning("HUD_HOST is not set")
            raise HudClientException("HUD_HOST is not set")
        user_options = get_user_options()
        if (
            not user_options
            or user_options.key is None
            or user_options.service is None
            or user_options.tags is None
        ):
            raise HudClientException("User options are not set")
        if is_async:
            return AsyncHttpClient(
                host, user_options.key, user_options.service, user_options.tags
            )
        return SyncHttpClient(
            host, user_options.key, user_options.service, user_options.tags
        )
    raise HudClientException("Unknown client type: {}".format(client_type))
