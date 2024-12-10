import json
import os
from typing import Dict, Optional, Union

from .logging import user_logger
from .users_logs import UsersLogs


class UserOptions:
    def __init__(
        self,
        key: Optional[str],
        service: Optional[str],
        tags: Optional[Union[Dict[str, str], str]],
        is_main_process: bool,
    ):
        self.key = self._get_key(key, is_main_process)
        self.service = self._get_service(service, is_main_process)
        self.tags = self._get_tags(tags, is_main_process)

    def _get_key(self, key: Optional[str], is_main_process: bool) -> Optional[str]:
        key = key or os.environ.get("HUD_KEY", None)
        if not key:
            if is_main_process:
                user_logger.log(*UsersLogs.HUD_KEY_NOT_SET)
            return None
        if not (isinstance(key, str) and key != ""):
            if is_main_process:
                user_logger.log(*UsersLogs.HUD_KEY_INVALID)
            return None
        return key

    def _get_service(
        self, service: Optional[str], is_main_process: bool
    ) -> Optional[str]:
        service = service or os.environ.get("HUD_SERVICE", None)
        if not service:
            if is_main_process:
                user_logger.log(*UsersLogs.HUD_SERVICE_NOT_SET)
            return None
        if not (isinstance(service, str) and service != ""):
            if is_main_process:
                user_logger.log(*UsersLogs.HUD_SERVICE_INVALID)
            return None
        return service

    def _get_tags(
        self, tags: Optional[Union[Dict[str, str], str]], is_main_process: bool
    ) -> Optional[Dict[str, str]]:
        try:
            tags = tags or os.environ.get("HUD_TAGS", "{}")
            if isinstance(tags, str):
                tags = json.loads(tags)
            if not (
                isinstance(tags, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str) for k, v in tags.items()
                )
            ):
                if is_main_process:
                    user_logger.log(*UsersLogs.HUD_TAGS_INVALID_TYPE)
                return {}

            if any("." in key for key in tags.keys()):
                if is_main_process:
                    user_logger.log(*UsersLogs.HUD_TAGS_WITH_DOTS)
                tags = {key.replace(".", "_"): value for key, value in tags.items()}
            return tags
        except Exception:
            if is_main_process:
                user_logger.log(*UsersLogs.HUD_TAGS_INVALID_JSON)
        return {}


_user_options = None  # type: Optional[UserOptions]


def init_user_options(
    key: Optional[str],
    service: Optional[str],
    tags: Optional[Union[Dict[str, str], str]],
    is_main_process: bool,
) -> UserOptions:
    global _user_options
    if _user_options:
        return _user_options

    _user_options = UserOptions(key, service, tags, is_main_process)
    return _user_options


def get_user_options() -> Optional[UserOptions]:
    return _user_options
