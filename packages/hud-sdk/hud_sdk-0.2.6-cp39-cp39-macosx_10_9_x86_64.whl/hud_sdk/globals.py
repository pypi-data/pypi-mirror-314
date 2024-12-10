from typing import TYPE_CHECKING, Optional  # noqa: F401

if TYPE_CHECKING:
    from .flow_metrics import FlowMetricsAggregator  # noqa: F401

metrics_aggregator = None  # type: Optional[FlowMetricsAggregator]
