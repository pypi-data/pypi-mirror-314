import os
import sys
from typing import Optional  # noqa: F401
from uuid import UUID

DEFAULT_HUD_HOST = "https://api-prod.hud.io"
DEFAULT_CLIENT = "http"
DEFAULT_DEBUG_PREFIX = "[HUD]"
DEFAULT_JSON_PATH = "hud.json"


class Config:
    def __init__(self) -> None:
        self.host = os.environ.get("HUD_HOST", DEFAULT_HUD_HOST)
        self.logs_queue_size = int(os.environ.get("HUD_LOGS_QUEUE_SIZE", 4000))
        self.batch_size = int(os.environ.get("HUD_BATCH_SIZE", 100))
        self.process_queue_flush_interval = int(
            os.environ.get("HUD_PROCESS_QUEUE_FLUSH_INTERVAL", 1)
        )
        self.logs_flush_interval = int(
            os.environ.get("HUD_LOGS_QUEUE_FLUSH_INTERVAL", 5)
        )
        self.invocations_flush_interval = int(
            os.environ.get("HUD_INVOCATIONS_FLUSH_INTERVAL", 30)
        )
        self.workload_data_flush_interval = int(
            os.environ.get("HUD_WORKLOAD_DATA_FLUSH_INTERVAL", 300)
        )
        self.modules_report_interval = int(
            os.environ.get("HUD_MODULES_REPORT_INTERVAL", 60 * 60)
        )
        self.performace_report_interval = int(
            os.environ.get("HUD_PERFORMANCE_REPORT_INTERVAL", 5 * 60)
        )
        self.declarations_flush_interval = int(
            os.environ.get("HUD_DECLARATIONS_FLUSH_INTERVAL", 5)
        )
        self.flow_metrics_flush_interval = int(
            os.environ.get("HUD_FLOW_METRICS_FLUSH_INTERVAL", 30)
        )
        self.api_max_retries = int(os.environ.get("HUD_API_MAX_RETRIES", 5))
        self.api_backoff_factor = float(os.environ.get("HUD_API_BACKOFF_FACTOR", 0.2))
        self.api_timeout = float(os.environ.get("HUD_API_TIMEOUT", 5))  # seconds
        self.debug_prefix = os.environ.get("HUD_DEBUG_PREFIX", DEFAULT_DEBUG_PREFIX)
        self.client_type = os.environ.get("HUD_CLIENT", DEFAULT_CLIENT)
        self.json_path = os.environ.get("HUD_JSON_PATH", DEFAULT_JSON_PATH)

        self.run_after_fork = sys.platform == "linux" and os.environ.get(
            "HUD_SUPPORT_FORK", "true"
        ).lower() in [
            "true",
            "1",
        ]

        modules_to_trace_str = os.environ.get("HUD_MODULES_TO_TRACE")
        self.modules_to_trace = (
            modules_to_trace_str.split(",") if modules_to_trace_str else []
        )
        self.blacklisted_modules = ["ddtrace", "opentelemetry-instrumentation"]
        self.log_level = os.environ.get("HUD_LOG_LEVEL", "INFO")
        self.verbose_logs = os.environ.get("HUD_VERBOSE", "").lower() in ["true", "1"]
        self.debug_logs = os.environ.get("HUD_DEBUG", "").lower() in ["true", "1"]
        self.pretty_logs = os.environ.get("HUD_PRETTY_LOGS", "false").lower() in [
            "true",
            "1",
        ]
        self.aws_metadata_server = os.environ.get(
            "HUD_AWS_METADATA_SERVER", "169.254.169.254"
        )
        self.aws_metadata_timeout = float(os.environ.get("HUD_AWS_METADATA_TIMEOUT", 5))
        self.aws_local_metadata_file = os.environ.get(
            "HUD_AWS_LOCAL_METADATA_FILE", "/run/cloud-init/instance-data.json"
        )
        self.disable_exception_handler = os.environ.get(
            "HUD_DISABLE_EXCEPTION_HANDLER", ""
        ).lower() in ["true", "1"]
        self.sketch_bin_width = float(os.environ.get("HUD_SKETCH_BIN_WIDTH", 1.2))
        self.log_performance = os.environ.get(
            "HUD_LOG_PERFORMANCE", "true"
        ).lower() not in [
            "false",
            "0",
        ]
        self.log_runtime = os.environ.get("HUD_LOG_RUNTIME", "true").lower() not in [
            "false",
            "0",
        ]

        self.instrument_fastapi = os.environ.get(
            "HUD_INSTRUMENT_FASTAPI", "true"
        ).lower() not in [
            "false",
            "0",
        ]
        self.instrument_flask = os.environ.get(
            "HUD_INSTRUMENT_FLASK", "true"
        ).lower() not in [
            "false",
            "0",
        ]
        self.uuid_namespace = UUID("f253e6fb-3f25-412c-907d-dbbbcc3f51c0}")
        self.sdk_name = "hud_sdk"

        self.exporter_start_timeout = 15
        self.exporter_service_registered_timeout = 10
        self.exporter_is_up_check_interval = 30

        self.exporter_shared_memory_size = 100_000_000
        self.exporter_process_registry_warmup_period = 5
        self.exporter_process_registry_update_interval = 1
        self.exporter_queue_process_interval = 0.1
        self.exporter_manager_check_interval = 10
        self.exporter_disabled_check_interval = 1

        self.manager_lock_warning_threshold = 1
        self.manager_lock_critical_threshold = 10
        self.manager_lock_owner_check_interval = 10

        self.manager_password = b"password"
        self.manager_initialization_timeout = 15

        self.shared_memory_utilization_warning_threshold = 50
        self.shared_memory_utilization_critical_threshold = 80
        self.shared_memory_utilization_check_interval = 60 * 3

        self.testing_output_directory = os.environ.get("HUD_TESTING_DIR", None)
        self.python_binary = os.environ.get(
            "HUD_PYTHON_BINARY_PATH", None
        )  # type: Optional[str]


config = Config()
