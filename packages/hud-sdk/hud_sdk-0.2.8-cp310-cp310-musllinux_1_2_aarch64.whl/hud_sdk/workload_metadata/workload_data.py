from typing import Optional

from ..config import config
from ..schemas.events import WorkloadData
from ..utils import suppress_exceptions_async
from .aws_workload_matadata import ImdsHttpClient, get_aws_workload_metadata
from .kubernetes_workload_metadata import get_kubernetes_workload_data


@suppress_exceptions_async(default_return_factory=lambda: WorkloadData())
async def get_workload_metadata(pod_cpu_limit: Optional[str] = None) -> WorkloadData:
    host_url = "http://{}".format(config.aws_metadata_server)
    timeout = config.aws_metadata_timeout
    imds_client = ImdsHttpClient(host_url, timeout)

    return WorkloadData(
        aws_workload_data=await get_aws_workload_metadata(imds_client),
        kubernetes_workload_data=get_kubernetes_workload_data(pod_cpu_limit),
    )
