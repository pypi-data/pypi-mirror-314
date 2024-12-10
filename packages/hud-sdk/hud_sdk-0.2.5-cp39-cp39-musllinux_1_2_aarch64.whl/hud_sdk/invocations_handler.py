import time
from datetime import datetime, timezone
from typing import List

from .native import check_linked_code, check_wrapped_code, get_and_swap_aggregations
from .schemas.events import Caller, Invocations, Sketch


class InvocationsHandler:
    def __init__(self) -> None:
        self.last_invocations_dump = time.perf_counter()

    def get_and_clear_invocations(self) -> List[Invocations]:
        current_time = time.perf_counter()
        timeslice = int(current_time - self.last_invocations_dump)
        self.last_invocations_dump = current_time
        invocations_c = get_and_swap_aggregations()
        if not invocations_c:
            return []

        invocations = [
            Invocations(
                count=invocation.total_calls,
                function_id=invocation.function_id,
                sampled_count=invocation.total_calls,
                sum_duration=invocation.total_time,
                sum_squared_duration=invocation.total_squared_time,
                timeslice=timeslice,
                timestamp=datetime.now(timezone.utc),
                callers=[
                    Caller(
                        name=c.co_name,
                        file_name=c.co_filename,
                        start_line=c.co_firstlineno,
                        is_wrapped=check_wrapped_code(c),
                    )
                    for c in invocation.callers
                    if c
                ],
                wrapped_flow_id=invocation.flow_id,
                exceptions=invocation.exceptions,
                sketch=(
                    Sketch(
                        bin_width=invocation.sketch_data.bin_width,
                        index_shift=invocation.sketch_data.index_shift,
                        data=invocation.sketch_data.data,
                    )
                    if invocation.sketch_data
                    else Sketch(bin_width=0, index_shift=0, data=[])
                ),
                is_linked_function=check_linked_code(invocation.code_obj),
            )
            for invocation in invocations_c.values()
        ]
        invocations_c.clear()
        return invocations
