import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

import aiohttp

from ..config import config
from ..logging import internal_logger
from ..schemas.events import AwsWorkloadData

if TYPE_CHECKING:
    from typing import Union  # noqa: F401


class AWSWorkloadError(Exception):
    pass


class ImdsClient(ABC):
    @abstractmethod
    async def get_instance_identity(self, **requests_kwargs: Any) -> Dict[str, str]:
        pass

    @abstractmethod
    async def get_instance_life_cycle(self, **requests_kwargs: Any) -> str:
        pass

    @abstractmethod
    async def gain_token(self, **requests_kwargs: Any) -> None:
        pass


class ImdsHttpClient(ImdsClient):
    def __init__(self, host: str, timeout: float) -> None:
        self.host = host
        self.token = None  # type: Optional[str]

        self.timeout = None  # type: Optional[Union[aiohttp.ClientTimeout, float]]
        if hasattr(aiohttp, "ClientTimeout"):
            self.timeout = aiohttp.ClientTimeout(timeout)
        else:
            self.timeout = timeout

        self.request_kwargs = {"timeout": self.timeout}  # type: Dict[str, Any]

    async def _get(self, url: str, **requests_kwargs: Any) -> aiohttp.ClientResponse:
        async with aiohttp.request(
            "GET", url, **self.request_kwargs, **requests_kwargs
        ) as response:
            response.raise_for_status()
            return response

    async def _put(self, url: str, **requests_kwargs: Any) -> str:
        async with aiohttp.request(
            "PUT", url, **self.request_kwargs, **requests_kwargs
        ) as response:
            response.raise_for_status()
            return await response.text()

    def _validate_token(self) -> None:
        if not self.token:
            raise AWSWorkloadError("Token is not set")

    async def get_instance_identity(self, **requests_kwargs: Any) -> Dict[str, str]:
        self._validate_token()
        res = await self._get(
            "{}/latest/dynamic/instance-identity/document".format(self.host),
            **requests_kwargs,
        )
        return cast(Dict[str, str], await res.json())

    async def get_instance_life_cycle(self, **requests_kwargs: Any) -> str:
        self._validate_token()
        res = await self._get(
            "{}/latest/meta-data/instance-life-cycle".format(self.host),
            **requests_kwargs,
        )
        return await res.text()

    def set_token(self, token: str) -> None:
        self.token = token
        self.request_kwargs["headers"] = {"X-aws-ec2-metadata-token": token}

    async def gain_token(self, **requests_kwargs: Any) -> None:
        headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token = await self._put(
            "{}/latest/api/token".format(self.host), headers=headers, **requests_kwargs
        )
        self.set_token(token)


async def get_imds_workload_metadata(imds_client: ImdsClient) -> AwsWorkloadData:
    await imds_client.gain_token()
    identity = await imds_client.get_instance_identity()
    life_cycle_data = await imds_client.get_instance_life_cycle()

    return AwsWorkloadData(
        ami_id=identity["imageId"],
        launched_date=identity["pendingTime"],
        life_cycle=life_cycle_data,
        region=identity["region"],
        workload_id=identity["instanceId"],
        workload_instance_type=identity["instanceType"],
    )


def get_local_aws_workload_metadata() -> AwsWorkloadData:
    local_metadata = Path(config.aws_local_metadata_file).read_text(encoding="utf8")
    local_metadata_parsed = json.loads(local_metadata)
    identity_parsed = local_metadata_parsed["ds"]["dynamic"]["instance-identity"][
        "document"
    ]
    return AwsWorkloadData(
        ami_id=identity_parsed["imageId"],
        launched_date=identity_parsed["pendingTime"],
        life_cycle=local_metadata_parsed["ds"]["meta-data"]["instance-life-cycle"],
        region=identity_parsed["region"],
        workload_id=identity_parsed["instanceId"],
        workload_instance_type=identity_parsed["instanceType"],
    )


async def get_aws_workload_metadata(
    imds_client: ImdsClient,
) -> Optional[AwsWorkloadData]:
    try:
        return get_local_aws_workload_metadata()
    except Exception as err:
        internal_logger.debug(
            "Failed to get workload metadata from local file with error: {}".format(err)
        )
    try:
        return await get_imds_workload_metadata(imds_client)
    except Exception as err:
        internal_logger.debug(
            "Failed to get workload metadata from IMDS with error: {}".format(err)
        )
    return None
