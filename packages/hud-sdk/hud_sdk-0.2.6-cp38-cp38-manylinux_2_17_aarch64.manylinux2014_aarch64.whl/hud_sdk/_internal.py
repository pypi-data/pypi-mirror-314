from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence  # noqa: F401

from .forkable import ForksafeSequence

worker_queue = ForksafeSequence(
    lambda: deque(maxlen=300000)
)  # type: ForksafeSequence[Sequence[Any]]
